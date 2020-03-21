from typing import NamedTuple

class TokenPair(NamedTuple):
    '''
    `TokenPair` is the pair of xsrf_token & csn.
    This pair is common for each chat component (list of chats
    fetched at one time).
    Separated from chat_param to reduce memory usage.
    
    '''
    xsrf_token: str
    #TODO: It seems that `csn` is unnesessary param.
    csn: str

class Token(NamedTuple):
    '''
    tokens & param for operating chats.
    `chat_param` is context menu parameter each chat has.
    '''
    token: TokenPair
    chat_param: str


class TokenList:
    '''
    TokenList is the list of tokens for operating chats.
        key : authorExternalChannelId
        value : tokens (xsrf_token & csn & contextMenuParams)
    '''

    def __init__(self):
        self._list = {}

    def add_token(self, chat, token: Token):
        self._list[chat.author_id] = token

    def get_token(self, author_id: str) -> Token:
        return self._list.get(author_id)