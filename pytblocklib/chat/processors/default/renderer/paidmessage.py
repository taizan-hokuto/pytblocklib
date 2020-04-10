import re
from .base import BaseRenderer

class LiveChatPaidMessageRenderer(BaseRenderer):
    def __init__(self, item):
        super().__init__(item, "superChat")

            
