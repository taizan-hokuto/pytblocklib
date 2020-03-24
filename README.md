# pytblocklib
## Overview
( **This project is under development.** )<br>
Pytblocklib is an library for blocking spam bots on YouTube.
<br>
<br>

Pytblocklib は、Youtubeのスパムボットのブロックを補助するライブラリです。<br>
YouTube API設定不要、リスナー側のブロックにも対応しています。<br>
詳細は[wiki](https://github.com/taizan-hokuto/pytblocklib/wiki) を参照してください。
<br>
+ このプロジェクトは開発中です。
+ YouTubeの仕様変更等により使用できなくなる場合があります。
+ ソースの使用に際しては自己責任でお願いいたします。
+ LICECNSE:GPL3
<br>

## Description
Pytblocklibs's goal is to provide easy blocking operation on YT.<br>
You can concentrate on thinking block algorithms.<br>
Function around livechat is based on my [pytchat](https://github.com/taizan-hokuto/pytchat) script.
<br>
<br>

## Features:
+ Functions focused on blocks, light weight, easy operation.
+ You can block as a listener. (not need to give or take moderator privileges)
+ No **S**craping, no **S**elenium, no Beautiful**S**oup.
 
 
## Usage
```python
from pytblocklib import Watcher
import time

w = Watcher("video_id")

NG_WORDS = ['NG_WORD1','NG_WORD2']
blocklist = []

w.start()

#Start checking loop
while w.loop():
    #Get chat list from buffer
    chats = w.get_chats()

    for chat in chats:
        for ng_word in NG_WORDS:
            if ng_word in chat.message or ng_word in chat.author_name:
                print("Found :message-`{}` by {} ".format(chat.message, chat.author_name))
                #Block user by specifying author channel id.
                w.block(chat.author_id)
                blocklist.append(chat.author_id)

    time.sleep(3)

#Example: Unblock all blocked users (only available during executing script)
for author_id in blocklist:
    w.unblock(author_id)
    

w.stop()

```

## VS

### [Nightbot](https://nightbot.tv/)
+ Pros 
+ + Sophisticated user interface on browser, integrated functions.
+ + Applicable for Twitch.
+ + Various blocking setting (e.g. blacklist, excess emotes, repetitions)
+ + Applicable to Twitch.

+ Cons
+ + Only srteamers can block spams on their broadcasting with moderator privileges, not per listener.

### [YouTube Studio](https://studio.youtube.com)
+ Pros 
+ + Official features.
+ + Various blocking setting (e.g. specify channel id, prohibited words)

+ Cons
+ + Only srteamers can block spams on their broadcasting with owner/moderator privileges, not per listener.


### Pytblocklib 
+ Pros 
+ + No need for YT API settings.
+ + Simple - functions focused on blocking spams.
+ + You can customize the blocking algorithm with a python script.
+ + You can block spams as a listener. (not need to give or take moderator privileges)

+ Cons
+ + Need to implement blocking procedures and user interface separately.
+ + Less portability : requires python environment. (planning to distribute as executable file)


## Requirements
browser_cookie3<br>
pytz<br>
requests<br>
urllib3<br>

## LICENSE
GNU GENERAL PUBLIC LICENSE Version 3



