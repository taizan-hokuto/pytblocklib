from .chat import LiveChat
from .blocker.blocker import Blocker
from .http.request import HttpRequest
from .chat.tokenlist import TokenList, Token
class Watcher:
    '''
    Watcher provides handles for fetching live chat and blocking operations.

    It can:
    + collect chat data in the background and store them in buffer.
    + fetch chats from buffer at any time (get() function) .
    + block and unblock the specified user.

    Note: LiveChat object derives from 
     pytchat(https://github.com/taizan-hokuto/pytchat).

    Parameters
    ----------
    video_id : str :
    seektime : int :
        Unit:seconds.
        Start position of fetching chat data.
        If negative value, try to fetch chat data
        posted before broadcast start.
    '''
    def __init__(self, video_id, seektime = -1):
        self._video_id = video_id
        self._req = HttpRequest()
        self._livechat = None
        self._blocker = None
        self._first_run = True
        self._tokenlist = TokenList()
        self._seektime = seektime

    def start(self):
        if self._first_run:
            self._first_run = False
            self._req = HttpRequest()
            self._livechat = LiveChat(
                self._video_id, req=self._req,
                tokenlist=self._tokenlist,
                seektime=self._seektime)
            self._blocker = Blocker(req=self._req, tokenlist=self._tokenlist)
        else:
            print("すでにチャット取得が開始されています。")

    def get_chats(self) -> list:
        if self._no_livechat(): return
        return self._livechat.get()

    def block(self, author_id:str) -> str:
        if self._no_livechat(): return
        return self._blocker.block(author_id)

    def unblock(self, author_id:str) -> str:
        if self._no_livechat(): return
        return self._blocker.unblock(author_id)

    def loop(self) -> bool:
        if self._first_run:
            self.start()
        return self._livechat.is_alive()

    def stop(self):
        LiveChat.shutdown(event=None)

    def _no_livechat(self):
        if self._first_run:
            print("ライブチャットが設定されていません。"
                  "最初にstart([動画ID])を呼び出す必要があります。")
            return True
        return False