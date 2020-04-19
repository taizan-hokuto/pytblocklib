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
+ YouTubeの仕様変更等により使用できなくなる場合があります。
+ 使用に際しては自己責任でお願いいたします。
+ [LICENSE](https://github.com/taizan-hokuto/pytblocklib/wiki#%E3%83%A9%E3%82%A4%E3%82%BB%E3%83%B3%E3%82%B9%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6):[LGPL-3.0](https://github.com/taizan-hokuto/pytblocklib/blob/master/LICENSE)
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
 
 
## Install
```
pip install pytblocklib
```

## Example
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
        if any(ng_word in chat.message or ng_word in chat.author_name  
            for ng_word in NG_WORDS):
            print("Found :message-`{}` by {} ".format(
                chat.message, chat.author_name))
            #Block user by specifying author channel id.
            w.block(chat.author_id)
            blocklist.append(chat.author_id)

    time.sleep(3)

#Example: Unblock all blocked users (only available during executing script)
for author_id in blocklist:
    w.unblock(author_id)
    

w.stop()

```

## Derived app
[AutoBlocker](https://github.com/Sayamame-beans/AutoBlocker) by [sayamame_beans](https://github.com/Sayamame-beans) <br>

## Compatible environment
+ Python 3.7.4 later
+ OS : Windows 10/ macOS Catarina / Ubuntu 18.04.2 LTS
+ Browser: Chrome v80 later / Firefox 75.0 later (requires browser cookie)



## VS

### [Nightbot](https://nightbot.tv/)
+ Pros 
+ + Sophisticated user interface on browser, integrated functions.
+ + Applicable for Twitch.
+ + Various blocking setting (e.g. blacklist, excess emotes, repetitions)

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
+ + Less portability : requires python environment.


## Using
This program uses a customized `browser_cookie3` library.<br>
The original copyright  of `browser_cookie 3` belongs to borisbabic : <br>
https://github.com/borisbabic/browser_cookie3<br>


## LICENSE
GNU LESSER GENERAL PUBLIC LICENSE Version 3



