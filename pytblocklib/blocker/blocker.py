
import json
import os
import re
import time
import urllib
from typing import NamedTuple
from .. import config
from ..chat.tokenlist import TokenList, Token
from ..http.request import HttpRequest
from ..util import get_item
from .serializer import Serializer

sejpath_listener = [
    "response",
    "liveChatItemContextMenuSupportedRenderers",
    "menuRenderer","items",2,
    "menuNavigationItemRenderer",
    "navigationEndpoint",
    "confirmDialogEndpoint",
    "content","confirmDialogRenderer",
    "confirmButton","buttonRenderer",
    "serviceEndpoint"
]

sejpath_author = [
    "response",
    "liveChatItemContextMenuSupportedRenderers",
    "menuRenderer","items",4,
    "menuServiceItemRenderer",
    "serviceEndpoint"
]

sejpath_author_alt = [
    "response",
    "liveChatItemContextMenuSupportedRenderers",
    "menuRenderer","items",5,
    "menuNavigationItemRenderer",
    "navigationEndpoint",
    "authServiceDialogEndpoint",
    "interface","authServiceDialogRenderer",
    "applyButton","buttonRenderer",
    "serviceEndpoint"
]

sejpath_unblock = [
    "data","actions",0,
    "liveChatAddToToastAction","item",
    "notificationActionRenderer",
    "actionButton","buttonRenderer",
    "serviceEndpoint"
]

sejpath_response_block_success = [
    "data","actions",0,
    "liveChatAddToToastAction","item",
    "notificationActionRenderer",
    "responseText","simpleText"
]

sejpath_response_unblock_success = [
    "data","actions",0,
    "liveChatAddToToastAction","item",
    "notificationTextRenderer",
    "successResponseText","simpleText"
]

class BlockItem(NamedTuple):
    '''
    BlockItem represents the item of blocked user and token for 
    unblock.
    '''
    key: str
    sej_unblock : dict
    token : Token

class Blocker:
    """
    Blocker blocks specified chatter.
    Block authority depends on browser cookie.
    """
    def __init__(self, req: HttpRequest, tokenlist:TokenList,
                logger = config.logger(__name__),):
        self.request = req
        self.blocked_list = {}
        self.unblocked_list = {}
        self.tokens = tokenlist
        self._logger = logger
        self._ser = None

    def _setup_blocklist_file(self):
        '''
        [DEPRECATE]
        Setup file to save blocklist and tokens temporarily.
        '''
        if os.path.exists('blocklst.temp'):
            os.remove('blocklst.temp')
        self._ser = Serializer('blocklst.temp')

    def _getContextMenuJson(self, params):
        url = f"https://www.youtube.com/live_chat/get_live_chat_item_context_menu?params={params}&pbj=1"
        resp = self.request.get(url=url)
        return json.loads(resp.text)

    def _getServiceEndPointListener(self, context_menu_json):
        serviceEndPoint = get_item(context_menu_json, sejpath_listener)
        return serviceEndPoint
       
    def _getServiceEndPointAuthor(self, context_menu_json):
        serviceEndPoint = get_item(context_menu_json, sejpath_author)
        return serviceEndPoint

    def _getServiceEndPointAuthorAlt(self, context_menu_json):
        serviceEndPoint = get_item(context_menu_json, sejpath_author_alt)
        return serviceEndPoint

    def block(self, key):
        '''
        Block specified listener's chats.
        
        Parameter
        ---------
        key : str :
            authorChannelId to block.
        '''

        if key in self.blocked_list:
            self._logger.info(f"{key}はすでにブロックリストに存在します。")
            return False
            
        #fetch session_token from tokenlist by authorChannelId
        _token = self.tokens.get_token(key)

        contextMenuJson = self._getContextMenuJson(_token.chat_param)

        '''When the `owner` (streamer) or moderator try to block someone
        in the broadcast, the structure of contextMenuJson is diffrent and 
        fail to parse. So we retry to parse the JSON with different path.
        '''
        serviceEndPoint = (
            self._getServiceEndPointListener(contextMenuJson) or 
            self._getServiceEndPointAuthor(contextMenuJson) or
            self._getServiceEndPointAuthorAlt(contextMenuJson)
        )

        if serviceEndPoint:
            resp = self._postparams(
                serviceEndPoint, _token.token.csn, _token.token.xsrf_token)
            resp = json.loads(resp.text)
            if resp.get("code") == "SUCCESS":
                #Store the params required for unblocking.
                sej_unblock = get_item(resp, sejpath_unblock)
                self._add_blocklist(sej_unblock, key, _token)
                self._logger.info(get_item(resp, sejpath_response_block_success))
                return True
        self._logger.info("ブロックできませんでした。")
        return False

    def _add_blocklist(self,sej_unblock, key, _token):
        #block_item = {"sej_unblock":sej_unblock, "token":_token}
        block_item = BlockItem(key=key,sej_unblock=sej_unblock, token=_token)
        self.blocked_list[key] = block_item
        self._logger.debug(f"{key}をブロックリストに追加しました")
    
    def _del_blocklist(self,key):
            result = self.blocked_list.pop(key)
            if result:
                self._logger.debug(f"ブロックリストから[{key}]を削除しました。")
            else:
                self._logger.error(f"ブロックリストに存在しないid({key})を削除しようとしました。")

    def _add_unblocklist(self,key):
        self.unblocked_list[key] = 1
        self._logger.debug(f"{key}をブロック解除リストに追加しました")

    def unblock(self, key):
        if key not in self.blocked_list:
            self._logger.error(f"{key}はブロック済みリストに存在しません。")
            return False
        
        sej_unblock = self.blocked_list[key].sej_unblock
        _token = self.blocked_list[key].token
        
        if sej_unblock is None or _token is None:
            self._logger.error("パラメータの復元に失敗しました")
            return False
        
        resp = self._postparams(
            sej_unblock, _token.token.csn, _token.token.xsrf_token
        )
        resp = json.loads(resp.text)
        if resp.get("code") == "SUCCESS":
            self._del_blocklist(key)
            self._logger.info(get_item(resp, sejpath_response_unblock_success))
            return True
        self._logger.error("セッション切断により自動ブロック解除に失敗しました。手動で解除してください")
        return False
        
    def _load_blocklist(self):
        '''
        [DEPRECATE]
        Load blocklist and tokens.
        '''
        items = self._ser.load()
        if items is None: return
        for item in items:
            self.blocked_list[item.key] = item

    def _postparams(self, sej, csn, xsrf_token):
        params = {
            "sej" : json.dumps(sej),
            "csn" : csn,
            "session_token": xsrf_token
        }
        url = "https://www.youtube.com/service_ajax?name=moderateLiveChatEndpoint"
        resp = self.request.post(url=url, params=params)
        return resp
