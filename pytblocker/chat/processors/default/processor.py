import asyncio
import time
from .renderer.base import BaseRenderer
from ... import config
from ...tokenlist import TokenList, Token, TokenPair

logger = config.logger(__name__)

class DefaultProcessor:

    def __init__(self, tokenlist: TokenList):
        self._tokens = tokenlist

    def process(self, chat_components: list):
        chatlist = []
        for component in chat_components or []:
            if component.get("tokendict"):
                _token_pair = TokenPair(component["tokendict"]["xsrf_token"],
                                        component["tokendict"]["csn"])
            else:
                _token_pair = TokenPair("","")
            chatdata = component.get('chatdata')
            if chatdata is None: continue
            for action in chatdata:
                chat = self._parse(action)
                if chat:
                    chatlist.append(chat)
                    _token = Token(_token_pair, chat.params)
                    self._tokens.add_token(chat, _token)
        return chatlist

    def _parse(self, sitem):
        if sitem is None: return None
        action = sitem.get("addChatItemAction")
        if action is None: return None
        item = action.get("item")
        if item is None: return None
        try:
            renderer = self._get_renderer(item)
            if renderer is None:
                return None

            renderer.get_snippet()
            renderer.get_authordetails()
            renderer.cleanup()
            
        except (KeyError,TypeError) as e:
            logger.error(f"{str(type(e))}-{str(e)} sitem:{str(sitem)}")
            return None
        return renderer        

    def _get_renderer(self, item):
        if item.get("liveChatTextMessageRenderer") or \
            item.get("liveChatPaidMessageRenderer") or \
            item.get( "liveChatPaidStickerRenderer") or \
            item.get("liveChatLegacyPaidMessageRenderer"):
            return BaseRenderer(item)
        return None