import re

import requests,os
from logTools.config import soipUrl

# 获取本机外网IP
def getInternetIP(headers):
    r=requests.get(soipUrl,headers=headers)
    beforeStr='user_ip="'
    endStr='";'
    s = r.text.find(beforeStr)
    e = r.text.find(endStr,s)
    return r.text[s+len(beforeStr):e]

# 获取文件大小
def getFileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)

# 待封装成一个日志分析类
def getIpInStr(logString):
    result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", logString)
    return result

def getOrPostApi(logString):
    pass