import os

# 钉钉机器人配置
isDingdingMsg=True
dingdingUrl='https://oapi.dingtalk.com/robot/send?access_token=0000000000000'
dingdingKeyword='logdatatar'

# 使用nginx配置的服务器可使用
isNginx=True
# 使用uwsgi配置的服务器可使用
isUwsgi=True # 需要在uwsgi.ini内配置master = true和touch-logreopen = /{log文件夹}}/touchforlog

# 《网络安全法第二十一条》第三款 采取监测、记录网络运行状态、网络安全事件的技术措施，并按照规定留存相关的网络日志不少于六个月
deleteDays=180

# 日志文件后缀名
fileType='.log'
# 获取当前文件夹作为日志文件夹
logFilePath=os.getcwd()
logFileList=list(filter(None, [f if os.path.splitext(f)[1] == fileType else '' for f in os.listdir(logFilePath)]))

# # # # # # # # # 其他基础配置# # # # # # # # #
# other basic config
headers={'Content-Type': 'application/json'}

# 搜狐接口获取本服务器外网IP
soipUrl='http://txt.go.sohu.com/ip/soip'