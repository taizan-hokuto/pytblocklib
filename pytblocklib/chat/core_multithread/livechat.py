import requests
import json
import signal
import time
import traceback
import urllib.parse
from concurrent.futures import CancelledError, ThreadPoolExecutor
from queue import Queue
from threading import  Event
from .buffer import Buffer
from .. import config
from ..exceptions  import ChatParseException,IllegalFunctionCall
from ..paramgen    import liveparam, arcparam
from ..parser.live import Parser
from ..processors.default.processor import DefaultProcessor
from ..tokenlist import TokenList, Token
from ...http.request import HttpRequest


MAX_RETRY = 10


class LiveChat:

    _setup_finished = False
    #チャット監視中のListenerのリスト
    _listeners = []

    def __init__(self, video_id,
                seektime = 0,
                processor = None,
                buffer = None,
                interruptable = True,
                callback = None,
                done_callback = None,
                force_replay = False,
                topchat_only  = False,
                logger = config.logger(__name__),
                req = None,
                tokenlist = None
                ):
        self._video_id  = video_id
        self._req = req
        self._logger = logger
        self._seektime = seektime
        self._processor = DefaultProcessor(tokenlist)
        if buffer is None:
            self._buffer = Buffer(maxsize = 100)
        else:
            self._buffer = buffer
        self._callback = callback
        self._done_callback = done_callback
        self._executor = ThreadPoolExecutor(max_workers=2)
        self._is_alive   = True
        self._is_replay = force_replay
        self._parser = Parser(is_replay = self._is_replay)
        self._pauser = Queue()
        self._pauser.put_nowait(None)
        self._first_fetch = True
        self._fetch_url = "live_chat/get_live_chat?continuation="
        self._topchat_only = topchat_only
        self._event = Event()


        LiveChat._logger = logger
        if not LiveChat._setup_finished:
            LiveChat._setup_finished = True
            if interruptable:
                signal.signal(signal.SIGINT,  (lambda a, b:  
                (LiveChat.shutdown(None,signal.SIGINT,b))
                ))
        LiveChat._listeners.append(self)


    def start(self):
        if self._callback is None:
            pass 
        else:
            self._executor.submit(self._callback_loop,self._callback)
        listen_task = self._executor.submit(self._startlisten)
        if self._done_callback is None:
            listen_task.add_done_callback(self.finish)
        else:
            listen_task.add_done_callback(self._done_callback)

    def _startlisten(self):
        time.sleep(0.1)  #sleep shortly to prohibit skipping fetching data
        """Fetch first continuation parameter,
        create and start _listen loop.
        """
        initial_continuation = liveparam.getparam(self._video_id,3)
        self._listen(initial_continuation)

    def _listen(self, continuation):

        ''' Fetch chat data and store them into buffer,
        get next continuaiton parameter and loop.

        Parameter
        ---------
        continuation : str
            parameter for next chat data
        '''
        try:
            with self._req.session as session:
                while(continuation and self._is_alive):
                    continuation = self._check_pause(continuation)
                    contents = self._get_contents(continuation, session)
                    metadata, chatdata =  self._parser.parse(contents)
                    timeout = metadata['timeoutMs']/1000
                    chat_component = {
                        "video_id" : self._video_id,
                        "timeout"  : timeout,
                        "chatdata" : chatdata,
                        "tokendict" : metadata.get("tokendict")
                    }
                    time_mark =time.time()
                    self._buffer.put(chat_component)
                    diff_time = timeout - (time.time()-time_mark)
                    self._event.wait(diff_time if diff_time > 0 else 0)
                    continuation = metadata.get('continuation')  
        except ChatParseException as e:
            self._logger.debug(f"[{self._video_id}]{str(e)}")
            return            
        except (TypeError , json.JSONDecodeError) :
            self._logger.error(f"{traceback.format_exc(limit = -1)}")
            return
        
        self._logger.debug(f"[{self._video_id}]finished fetching chat.")

    def _check_pause(self, continuation):
        if self._pauser.empty():
            '''pause'''
            self._pauser.get()
            '''resume:
                prohibit from blocking by putting None into _pauser.
            '''
            self._pauser.put_nowait(None)
            if not self._is_replay:
                continuation = liveparam.getparam(self._video_id,3)
        return continuation

    def _get_contents(self, continuation, session):
        '''Get 'continuationContents' from livechat json.
           If contents is None at first fetching, 
           try to fetch archive chat data.

          Return:
          -------
            'continuationContents' which includes metadata & chat data.
        '''
        livechat_json = ( 
            self._get_livechat_json(continuation, session)
        )
        contents = self._parser.get_contents(livechat_json)
        if self._first_fetch:
            if contents is None or self._is_replay:
                '''Try to fetch archive chat data.'''
                self._parser.is_replay = True
                self._fetch_url = "live_chat_replay/get_live_chat_replay?continuation="
                continuation = arcparam.getparam(
                    self._video_id, self._seektime, self._topchat_only)
                livechat_json = (self._get_livechat_json(continuation, session))
                reload_continuation = self._parser.reload_continuation(
                    self._parser.get_contents(livechat_json))
                if reload_continuation:
                    livechat_json = (self._get_livechat_json(
                        reload_continuation, session))
                contents = self._parser.get_contents(livechat_json)
                self._is_replay = True
            self._first_fetch = False
        return contents

    def _get_livechat_json(self, continuation, session):
        '''
        Get json which includes chat data.
        '''
        continuation = urllib.parse.quote(continuation)
        livechat_json = None
        status_code = 0
        url =f"https://www.youtube.com/{self._fetch_url}{continuation}&pbj=1"
        for _ in range(MAX_RETRY + 1):
            with session.get(url) as resp:
                try:
                    text = resp.text
                    livechat_json = json.loads(text)
                    break
                except json.JSONDecodeError :
                    time.sleep(1)
                    continue
        else:
            self._logger.error(f"[{self._video_id}]"
                    f"Exceeded retry count. status_code={status_code}")
            return None
        return livechat_json
  
    def _callback_loop(self,callback):
        """ コンストラクタでcallbackを指定している場合、バックグラウンドで
        callbackに指定された関数に一定間隔でチャットデータを投げる。        
        
        Parameter
        ---------
        callback : func
            加工済みのチャットデータを渡す先の関数。
        """
        while self.is_alive():
            items = self._buffer.get()
            processed_chat = self._processor.process(items)
            if isinstance(processed_chat, tuple):
                self._callback(*processed_chat)
            else:
                self._callback(processed_chat)

    def get(self):
        """ bufferからデータを取り出し、processorに投げ、
        加工済みのチャットデータを返す。
        
        Returns
             : Processorによって加工されたチャットデータ
        """
        if self._callback is None:
            items = self._buffer.get()
            return  self._processor.process(items)
        raise IllegalFunctionCall(
            "既にcallbackを登録済みのため、get()は実行できません。")

    def is_replay(self):
        return self._is_replay

    def pause(self):
        if self._callback is None:
            return
        if not self._pauser.empty():
            self._pauser.get()

    def resume(self):
        if self._callback is None:
            return
        if self._pauser.empty():
            self._pauser.put_nowait(None)
        
    def is_alive(self):
        return self._is_alive

    def finish(self,sender):
        '''Listener終了時のコールバック'''
        try: 
            self.terminate()
        except CancelledError:
            self._logger.debug(f'[{self._video_id}]cancelled:{sender}')

    def terminate(self):
        '''
        Listenerを終了する。
        '''
        self._is_alive = False
        self._logger.info(f'[{self._video_id}]終了しました')
  
    @classmethod
    def shutdown(cls, event, sig = None, handler=None):
        for t in LiveChat._listeners:
            t._logger.debug("shutdown...")
            t._is_alive = False
            t._event.set()