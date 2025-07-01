import os
# 配置文件部分
modelDic={
    # 参数名 :(命令缩写，msg功能描述，默认值)
    'durl':('url','配置钉钉机器人url','https://oapi.dingtalk.com/'),
    'dingtalk':('d','钉钉通知开关','TRUE'),
    'dkeyword':('k','配置钉钉自定义关键词','logdatatar'),
    'warnsize':('w', '配置单日志文件大小告警值，单位MB','500'),
    # 《网络安全法第二十一条》第三款 采取监测、记录网络运行状态、网络安全事件的技术措施，并按照规定留存相关的网络日志不少于六个月
    'days':('day','日志删除天数','200'),
    'nginx':('n','使用nginx配置的服务器可使用','TRUE'),
    'uwsgi':('u','使用uwsgi配置 需要在uwsgi.ini内配置master=true和touch-logreopen=/{log文件夹}/touchforlog','TRUE'),
    'file':('f','日志文件后缀名','.log'),
    'lastlines':('l','读取日志文件最后n行提供listener.py判断','10000'),
    'secondmax':('m','1秒钟同时请求大于m条，告警，同时作为报文倍数分组step使用','3'),
    'withoutlog':('o','配置忽略log文件名使用,分割，demo:c1.log,c2.log',''),
}
configFileName='./.pylogconfig'
def getConfigDic(path):
    configDic={}
    if os.path.exists(path):
        f = open(path, 'r')
        for line in f:
            if ' ' in line:
                l = line.split(' ')
                if len(l) >= 2:
                    configDic[l[0]] = l[1]
        f.close()
    return configDic
configDic = getConfigDic(path=configFileName)

def getConfigVaule(key,configDic=configDic):
    output = configDic[key] if key in configDic else modelDic[key][2]
    if output.upper() in ['FALSE','TRUE']:
        return ['FALSE','TRUE'].index(output.upper())
    else:
        return output

isDingtalkMsg = getConfigVaule('dingtalk')
durl = getConfigVaule('durl').strip() # 添加strip防止复制时空格回车干扰
dkeyword = getConfigVaule('dkeyword') # 在钉钉robot里面设置自定义关键词，保证消息可以到达钉钉
warnsize = float(getConfigVaule('warnsize'))
deleteDays = int(getConfigVaule('days'))
isNginx = getConfigVaule('nginx')  # 使用nginx配置的服务器可使用
isUwsgi = getConfigVaule('uwsgi')  #
fileType = getConfigVaule('file')
lastLinesNum=int(getConfigVaule('lastlines'))
oneSecondMaxlog=int(getConfigVaule('secondmax'))
withoutLogList = getConfigVaule('withoutlog').split(',')

# 检测并安装requests 为钉钉通知提供服务
if isDingtalkMsg:
    try:
        import requests
    except:
        os.system('pip3 install requests')
        import requests

# 获取当前文件夹作为日志文件夹
logFilePath = os.getcwd()
logFileList = list(filter(None, [f if os.path.splitext(f)[1] == fileType else '' for f in os.listdir(logFilePath)]))
logFileList = list(set(logFileList)-set(withoutLogList))
# # # # # # # # # 其他基础配置 # # # # # # # # #
# other basic config
headers={'Content-Type': 'application/json'}
soipUrl = 'http://txt.go.sohu.com/ip/soip'  # 搜狐接口获取本服务器外网IP
fileNameDelimiter='_'
delimiter=' - '
dingtalkMsgContentCut=15000

