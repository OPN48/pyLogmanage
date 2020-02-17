# pyLogmanage
A python lite log manage open repository

1.compress logs file

   move the project file to your logs path, and adding a cronjob to run logdatatar.py
```
cd {your logs path} && python3 logdatatar.py
```
like:
```
cd /home/log && python3 logdatatar.py
```
**uWSGI setting:**

open your uWSGI settings file uwsgi.ini , and add:
```
[uwsgi]
master = true
touch-logreopen = {your logs path}/touchforlog
```
2.dingtalk msg
open ./logTools/config.py and setting your dingtalk robot, demo:
```
isDingdingMsg = True 
dingdingUrl = 'https://oapi.dingtalk.com/robot/send?access_token=0000000000000'
dingdingKeyword = 'logdatatar'
```

