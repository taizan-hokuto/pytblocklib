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

## VS (competitive solution)

### [Nightbot](https://nightbot.tv/)
+ Pros 
+ + Sophisticated user interface on browser, integrated functions.
+ + Applicable for Twitch.
+ + Various blocking setting (blacklist, excess emotes, repetitions etc...)
+ + Applicable to Twitch.

+ Cons
+ + Nightbot exercises the block with moderator privileges
over the program being broadcast.
not block spams per listener.

### [YouTube Studio](https://studio.youtube.com)
+ Pros 
+ + Official features.
+ + Various blocking setting (Specify channel id, prohibited word etc...)

+ Cons
+ + It is possible to block only as an author.
not to block spams per listener, per .
+ + The setting menu is complicated and messy with other features.

### Pytblocker (Goal)
+ Pros 
+ + Functions focused on blocks, light weight, easy operation.
+ + You can customize the details with a python script.

+ Cons
+ + User interface (For now, planning CUI)
+ + Portability (python environment). 
(Compile and distribute as executable?)


## Requirements
browser_cookie3
pytz
requests
urllib3



