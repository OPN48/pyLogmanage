# pyLogmanage
A python lite log manage open repository, rotate your log files and send the msg to your dingtalk.

1.how to install:

you can use the git command clone this repository in to your logs path:
```
cd {your log path}

git clone --recursive https://github.com/OPN48/pyLogmanage.git && mv ./pyLogmanage/* ./ && mv ./pyLogmanage/.git ./.git && mv ./pyLogmanage/.gitignore ./.gitignore && rm -rf ./pyLogmanage
```
If you don't want clone in your logs path, and than you would be change the logFilePath and the logFileList values in  ./logTools/config.py
```buildoutcfg
logFilePath = os.getcwd()
logFileList = list(filter(None, [f if os.path.splitext(f)[1] == fileType else '' for f in os.listdir(logFilePath)]))
```

2.setting pyLogmanage:

```
$ python3 setup.py 
用法: python3 setup.py [-options] [args...](执行初始化配置)
    -url -durl    	配置钉钉机器人url 默认:https://oapi.dingtalk.com/
    -d -dingtalk    	钉钉通知开关 默认:TRUE
    -k -dkeyword    	配置钉钉自定义关键词 默认:logdatatar
    -w -warnsize    	配置单日志文件大小告警值，单位MB 默认:500
    -day -days    	日志删除天数 默认:180
    -n -nginx    	使用nginx配置的服务器可使用 默认:TRUE
    -u -uwsgi    	使用uwsgi配置 需要在uwsgi.ini内配置master=true和touch-logreopen=/{log文件夹}/touchforlog 默认:TRUE
    -f -file    	日志文件后缀名 默认:.log
    -l -lastlines    	读取日志文件最后n行提供listener.py判断 默认:1000
    -m -secondmax    	1秒钟同时请求大于m条，告警，同时作为报文倍数分组step使用 默认:3

```
setting you dingtalk url:
```
$ python3 setup.py -url https://oapi.dingtalk.com/robo...
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
You will receive a msg on you dingtalk group, like this:
```
【xxx.xxx.xxx.xx】：
xxx_nginx_access.log 173.66MB
xxx_uwsgi.log 1.33MB
log-2020-01-01.tar.gz 50.33MB
```
4.listener logs
adding a cronjob to run listener.py
```
cd {your logs path} && python3 listener.py
```
like:
```
cd /home/log && python3 listener.py
```
You will receive a msg on you dingtalk group, like this:
```
【xxx.xxx.xxx.xx】The Last 1000 lines log:
【more than 3/s】:
xxx//api/get/?
```