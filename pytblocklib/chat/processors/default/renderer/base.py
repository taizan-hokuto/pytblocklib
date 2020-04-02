from datetime import datetime

class Author:
    pass


class BaseRenderer:
    def __init__(self, item):
        self.renderer = list(item.values())[0]

    def get_snippet(self):
        self.id = self.renderer.get('id')
        timestampUsec = int(self.renderer.get("timestampUsec",0))
        self.timestamp = int(timestampUsec/1000)
        self.datetime = self.get_datetime(timestampUsec)
        self.message = self.get_message(self.renderer)
        self.params = self.renderer["contextMenuEndpoint"]["liveChatItemContextMenuEndpoint"]["params"]

    def get_authordetails(self):
        self.author_id = self.renderer.get("authorExternalChannelId")
        self.author_name      = self.renderer["authorName"]["simpleText"]


    def get_message(self,renderer):
        message = ''
        if renderer.get("message"):
            runs=renderer["message"].get("runs")
            if runs:
                for r in runs:
                    if r:
                        if r.get('emoji'):
                            message += r['emoji'].get('shortcuts',[''])[0]
                        else:
                            message += r.get('text','')
        return message
    

    def get_datetime(self,timestamp):
        dt = datetime.fromtimestamp(timestamp/1000000)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    def cleanup(self):
        self.renderer = None