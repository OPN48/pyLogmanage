import os
VERSION_NAME = 'v1.0.3'
IP_APIS = ['https://httpbin.org/ip','https://ifconfig.me/ip', 'https://ident.me', 'https://icanhazip.com']

IP = 'ip'
WITHOUTLOG = 'withoutlog'
SECONDMAX = 'secondmax'
LASTLINES = 'lastlines'
FILE = 'file'
UWSGI = 'uwsgi'
NGINX = 'nginx'
DAYS = 'days'
WARNSIZE = 'warnsize'
DKEYWORD = 'dkeyword'
DURL = 'durl'
DINGTALK = 'dingtalk'

IP_DEFAULT_NAME = 'update'
# # # # # # # # # 其他基础配置 # # # # # # # # #
# other basic config
HEADERS = {'Content-Type': 'application/json'}
FILENAME_DELIMITER = '_'
DELIMITER = ' - '
DINGTALK_MSG_CONTENT_CUT=15000
CONFIG_FILENAME= './.pylogconfig'
LOG_FILE_EXTENSION = '.tar.gz'
LOG_FILE_PREFIX = 'log-'

# 配置文件部分
modelDic={
    # 参数名 :(命令缩写，msg功能描述，默认值)
    DURL:('url', '配置钉钉机器人url', 'https://oapi.dingtalk.com/'),
    DINGTALK:('d', '钉钉通知开关', 'TRUE'),
    DKEYWORD:('k', '配置钉钉自定义关键词', 'logdatatar'),
    WARNSIZE:('w', '配置单日志文件大小告警值，单位MB', '500'),
    # 《网络安全法第二十一条》第三款 采取监测、记录网络运行状态、网络安全事件的技术措施，并按照规定留存相关的网络日志不少于六个月
    DAYS:('day', '日志删除天数', '200'),
    NGINX:('n', '使用nginx配置的服务器可使用', 'TRUE'),
    UWSGI:('u', '使用uwsgi配置 需要在uwsgi.ini内配置master=true和touch-logreopen=/{log文件夹}/touchforlog', 'TRUE'),
    FILE:('f', '日志文件后缀名', '.log'),
    LASTLINES:('l', '读取日志文件最后n行提供listener.py判断', '10000'),
    SECONDMAX:('m', '1秒钟同时请求大于m条，告警，同时作为报文倍数分组step使用', '3'),
    WITHOUTLOG:('o', '配置忽略log文件名使用,分割，demo:c1.log,c2.log', ''),
    IP: (IP, '配置本机外网ip，自更新', IP_DEFAULT_NAME)
}

def getConfigDic(path):
    configDic={}
    if os.path.exists(path):
        f = open(path, 'r')
        for line in f:
            line = line.strip()
            if ' ' in line:
                l = line.split(' ')
                if len(l) >= 2:
                    configDic[l[0]] = l[1]
        f.close()
    return configDic
configDic = getConfigDic(path=CONFIG_FILENAME)

def getConfigVaule(key,configDic=configDic):
    output = configDic[key] if key in configDic else modelDic[key][2]
    if output.upper() in ['FALSE','TRUE']:
        return ['FALSE','TRUE'].index(output.upper())
    else:
        return output


isDingtalkMsg = getConfigVaule(DINGTALK)
durl = getConfigVaule(DURL).strip() # 添加strip防止复制时空格回车干扰
dkeyword = getConfigVaule(DKEYWORD) # 在钉钉robot里面设置自定义关键词，保证消息可以到达钉钉
warnsize = float(getConfigVaule(WARNSIZE))
deleteDays = int(getConfigVaule(DAYS))
isNginx = getConfigVaule(NGINX)  # 使用nginx配置的服务器可使用
isUwsgi = getConfigVaule(UWSGI)  #
fileType = getConfigVaule(FILE)
lastLinesNum = int(getConfigVaule(LASTLINES))
oneSecondMaxlog = int(getConfigVaule(SECONDMAX))
withoutLogList = getConfigVaule(WITHOUTLOG).strip().split(',')
ip = getConfigVaule(IP)
headerText=f'【{ip}】 {VERSION_NAME}：\n\n'
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
# -o withoutLog clean
# print(logFileList)
needListenerLogFileList = list(set(logFileList)-set(withoutLogList))



