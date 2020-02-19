# pyLogmanage
A python lite log manage open repository, rotate your log files and send the msg to your dingtalk.

1.how to install:

you can use vi touch a restart.sh in you logs path:
```
$ vi restart.sh
```
and input:
```
rm -rf ./logTools
sleep 1
git clone --recursive https://github.com/OPN48/pyLogmanage.git
sleep 1
yes | mv ./pyLogmanage/* ./
sleep 1
rm -rf ./pyLogmanage
``` 

after that, don't forget use chmod  777 to give it permission and run
```
$ chmod 777 ./restart.sh
$ ./restart.sh
```

2.setting dingtalk url:

You can use the vi ./logTools/config.py
```
$vi ./logTools/config.py
```
and setting your dingtalk robot config, demo:
```
isDingdingMsg = True 
dingdingUrl = 'https://oapi.dingtalk.com/robot/send?access_token=0000000000000'
dingdingKeyword = 'logdatatar'
```
or use the setup.py
```
$ python3 setup.py https://oapi.dingtalk.com/robot/send?access_token=0000000000000
```

3.compress logs file

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