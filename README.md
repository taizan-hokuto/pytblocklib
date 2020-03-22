# pytblocker
## Overview
( **This project is under development.** )<br>
Pytblocker is an engine for blocking spam bots on YouTube.

## Description
Pytblockers's goal is to provide easy blocking and unblocking operation on YT.<br>
You can concentrate on thinking block algorithms.<br>
Function around livechat is based on my [pytchat](https://github.com/taizan-hokuto/pytchat) script.
<br>
<br>

## Features (goal):
+ Functions focused on blocks, light weight, easy operation.
+ No **S**craping, no **S**elenium, no Beautiful**S**oup.

## Usage
```python
from pytblocker import Watcher
import time

w = Watcher("video_id")

NG_WORDS = ['NG_WORD1','NG_WORD2']
blocklist = []

w.start()

#Start checking loop
while w.loop():
    #Get chat data from buffer
    chats = w.get_chats()

    if len(chats)==0:
        continue

    for chat in chats:
        for ng_word in NG_WORDS:
            if ng_word in chat.message:
                print("Found :message-`{}` by {} ".format(chat.message, chat.author_name))
                #Block user by specifying author channel id.
                result = w.block(chat.author_id)
                print(result)
                blocklist.append(chat.author_id)

    time.sleep(3)

#Example: Unblock all blocked users
for author_id in blocklist:
    result = w.unblock(author_id)
    print(result)

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


### Pytblocker (Goal)
+ Pros 
+ + No need for YT API settings.
+ + Simple - functions focused on blocking spams.
+ + You can customize the blocking algorithm with a python script.
+ + You can block spams as a listener. (not need to give or take moderator privileges)

+ Cons
+ + Poor user interface. (planning to GUI)
+ + Less portability : requires python environment. (planning to distribute as executable file)


## Requirements
browser_cookie3<br>
pytz<br>
requests<br>
urllib3<br>

## LICENSE
GNU GENERAL PUBLIC LICENSE Version 3



