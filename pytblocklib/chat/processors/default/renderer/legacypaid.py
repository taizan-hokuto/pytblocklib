from .base import BaseRenderer
class LiveChatLegacyPaidMessageRenderer(BaseRenderer):
    def __init__(self, item):
        super().__init__(item, "new_member")
       
    def get_authordetails(self):
        super().get_authordetails()
        self.is_member =  True

    def get_message(self,renderer):
        message = (renderer["eventText"]["runs"][0]["text"]
            )+' / '+(renderer["detailText"]["simpleText"])
        return message


