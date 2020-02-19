# pyLogmanage
A python lite log manage open repository, rotate your log files and send the msg to your dingtalk.

1.how to install:

you can use the git command clone that repository in to your logs path:
```
$cd {your log path}
$git clone --recursive https://github.com/OPN48/pyLogmanage.git
$mv ./pyLogmanage/* ./ 
$mv ./pyLogmanage/.git ./.git
$mv ./pyLogmanage/.gitignore ./.gitignore
$rm -rf ./pyLogmanage
```
If you don't want clone in your logs path, and than you would be change the logFilePath and the logFileList values in  ./logTools/config.py
```buildoutcfg
logFilePath = os.getcwd()
logFileList = list(filter(None, [f if os.path.splitext(f)[1] == fileType else '' for f in os.listdir(logFilePath)]))
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

open your uWSGI settings file uwsgi.ini , and add this:
```
[uwsgi]
master = true
touch-logreopen = {your logs path}/touchforlog
```