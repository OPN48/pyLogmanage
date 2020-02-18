import os
# 钉钉机器人配置
isDingtalkMsg = True
try:
    # 文件读取形式，方便重复拉取
    f=open('./dingtalkUrl','r')
    for line in f:
        if 'dingdingUrl' in line:
            dingdingUrl=line.split(' ')[1]
except:
    dingdingUrl = 'https://oapi.dingtalk.com/robot/send?access_token=0000000000000'
dingdingKeyword = 'logdatatar'  # 在钉钉robot里面设置自定义关键词，保证消息可以到达钉钉

# 检测并安装requests 为钉钉通知提供服务
if isDingtalkMsg:
    try:
        import requests
    except:
        os.system('pip3 install requests')
        import requests

isNginx = True  # 使用nginx配置的服务器可使用
isUwsgi = True   # 使用uwsgi配置的服务器可使用  需要在uwsgi.ini内配置master = true和touch-logreopen = /{log文件夹}}/touchforlog

deleteDays = 180  # 《网络安全法第二十一条》第三款 采取监测、记录网络运行状态、网络安全事件的技术措施，并按照规定留存相关的网络日志不少于六个月

# 日志文件后缀名
fileType = '.log'
# 获取当前文件夹作为日志文件夹
logFilePath = os.getcwd()
logFileList = list(filter(None, [f if os.path.splitext(f)[1] == fileType else '' for f in os.listdir(logFilePath)]))

lastLinesNum=3000
oneMinMaxlog=3

# # # # # # # # # 其他基础配置# # # # # # # # #
# other basic config
headers={'Content-Type': 'application/json'}
soipUrl = 'http://txt.go.sohu.com/ip/soip'  # 搜狐接口获取本服务器外网IP

