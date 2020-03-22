
import json
import re
import time
import urllib
from ..chat.tokenlist import TokenList, Token
from ..http.request import HttpRequest
from ..util import get_item



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
class Blocker:
    """
    Blocker blocks specified YouTube chatter.
    Block authority depends on browser cookie.
    (Current version Chrome only)
    """
    def __init__(self, req: HttpRequest, tokenlist:TokenList):
        self.request = req
        self.blocked_list = {}
        self.unblocked_list = {}
        self.tokens = tokenlist
       
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

    def block(self, author_id):
        '''
        Block specified listeners's chats.
        
        Parameter
        ---------
        author_id : str :
            authorChannelId to block.
        '''

        if author_id in self.blocked_list:
            return (f"{author_id}はすでにブロックリストに存在します。")
            
        #fetch session_token from tokenlist by authorChannelId
        _token = self.tokens.get_token(author_id)

        contextMenuJson = self._getContextMenuJson(_token.chat_param)
        serviceEndPoint = self._getServiceEndPointListener(contextMenuJson)

        '''Even if the `owner` (streamer) or moderator try to block someone
        in the broadcast, the structure of contextMenuJson is diffrent and 
        fail to parse. So we retry to parse the JSON with different path.
        '''
        if serviceEndPoint is None:
            serviceEndPoint = self._getServiceEndPointAuthor(contextMenuJson)

        resp = self._postparams(
            serviceEndPoint, _token.token.csn, _token.token.xsrf_token)
        resp = json.loads(resp.text)
        if resp.get("code") == "SUCCESS":
            #Stores params required for unblocking.
            sej_unblock = get_item(resp, sejpath_unblock)
            self._add_blockedlist(sej_unblock, author_id, _token)
            return get_item(resp, sejpath_response_block_success)
        return "ブロックできませんでした。"

    def _add_blockedlist(self,sej_unblock, author_id, _token):
        self.blocked_list[author_id] = {"sej_unblock":sej_unblock, "token":_token}
        return f"{author_id}をブロックリストに追加しました"
    
    def _del_blockedlist(self,author_id):
            result = self.blocked_list.pop(author_id)
            if result:
                return f"ブロックリストから{author_id}を削除しました。"
            else:
                return f"ブロックリストに存在しないid{author_id}を削除しようとしました。"

    def _add_unblockedlist(self,author_id):
        self.unblocked_list[author_id] = 1
        return f"{author_id}をブロック解除リストに追加しました"
        

    def unblock(self, author_id):
        if author_id not in self.blocked_list:
            return f"{author_id}はブロック済みリストに存在しません。"
        
        sej_unblock = self.blocked_list[author_id].get("sej_unblock")
        _token = self.blocked_list[author_id].get("token")
        
        if sej_unblock is None or _token is None:
            return "パラメータの復元に失敗しました"
        
        resp = self._postparams(
            sej_unblock, _token.token.csn, _token.token.xsrf_token
        )
        resp = json.loads(resp.text)
        if resp.get("code") == "SUCCESS":
            self._del_blockedlist(author_id)
            return get_item(resp, sejpath_response_unblock_success)
        return "ブロック解除できませんでした。"
        

    def _postparams(self, sej, csn, xsrf_token):
        params = {
            "sej" : json.dumps(sej),
            "csn" : csn,
            "session_token": xsrf_token
        }
        url = "https://www.youtube.com/service_ajax?name=moderateLiveChatEndpoint"
        resp = self.request.post(url=url, params=params)
        return resp
