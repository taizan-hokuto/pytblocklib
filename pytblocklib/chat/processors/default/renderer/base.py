from datetime import datetime

class BaseRenderer:
    def __init__(self, item, chattype):
        self.renderer = list(item.values())[0]
        self.chattype = chattype

    def get_snippet(self):
        self.type = self.chattype
        self.id = self.renderer.get('id')
        timestampUsec = int(self.renderer.get("timestampUsec",0))
        self.timestamp = int(timestampUsec/1000)
        tst = self.renderer.get("timestampText")
        if tst:
            self.elapsed = tst.get("simpleText")
        else:
            self.elapsed = ""
        self.datetime = self.get_datetime(timestampUsec)
        self.message ,self.message_ex = self.get_message(self.renderer)
        self.id =  self.renderer.get('id')
        self.bg_color = 0
        self.params = self.renderer["contextMenuEndpoint"]["liveChatItemContextMenuEndpoint"]["params"]

    def get_authordetails(self):
        self.author_badge = ""
        (self.is_verified, 
        self.is_owner, 
        self.is_member, 
        self.is_moderator) = (
            self.get_badges(self.renderer)
        )
        self.author_id = self.renderer.get("authorExternalChannelId")
        self.author_channel = "http://www.youtube.com/channel/"+self.author_id
        self.author_name      = self.renderer["authorName"]["simpleText"]
        self.author_image= self.renderer["authorPhoto"]["thumbnails"][1]["url"] 
        

    def get_message(self,renderer):
        message = ''
        message_ex = []
        if renderer.get("message"):
            runs=renderer["message"].get("runs")
            if runs:
                for r in runs:
                    if r:
                        if r.get('emoji'):
                            message += r['emoji'].get('shortcuts',[''])[0]
                            message_ex.append(r['emoji']['image']['thumbnails'][1].get('url'))
                        else:
                            message += r.get('text','')
                            message_ex.append(r.get('text',''))
        return message, message_ex


    def get_badges(self,renderer):
        is_verified = False
        is_owner = False
        is_member = False
        is_moderator = False
        badges=renderer.get("authorBadges")
        if badges:
            for badge in badges:
                if badge["liveChatAuthorBadgeRenderer"].get("icon"):
                    author_type  = badge["liveChatAuthorBadgeRenderer"]["icon"]["iconType"]
                    if author_type == 'VERIFIED':
                        is_verified = True
                    if author_type == 'OWNER':
                        is_owner = True
                    if author_type == 'MODERATOR':
                        is_moderator = True
                if badge["liveChatAuthorBadgeRenderer"].get("customThumbnail"):
                    is_member = True
                    self.get_badgeurl(badge)
        return is_verified, is_owner, is_member, is_moderator
    

    def get_badgeurl(self,badge):
        self.author_badge = badge["liveChatAuthorBadgeRenderer"]["customThumbnail"]["thumbnails"][0]["url"]


    def get_datetime(self,timestamp):
        dt = datetime.fromtimestamp(timestamp/1000000)
        return dt.strftime('%Y-%m-%d %H:%M:%S')


    def cleanup(self):
        self.renderer = None