from .base import BaseRenderer


class LiveChatPaidMessageRenderer(BaseRenderer):
    def __init__(self, item):
        super().__init__(item, "super_chat")

    def get_snippet(self):
        super().get_snippet()
        self.amount_string = self.renderer["purchaseAmountText"]["simpleText"]
        self.bg_color = self.renderer.get("bodyBackgroundColor", 0)
        self.txt_color = self.renderer.get("bodyTextColor", 0)