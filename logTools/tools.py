import re,json
from logTools.config import *

# 获取文件大小
def getFileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)
# 前后特征输出
def lineLookup(s, frontStr, behindStr):
    beginNum= s.find(frontStr) + len(frontStr)
    endNum=s.find(behindStr,beginNum)
    result=''
    if endNum != -1 and s.find(frontStr) != -1 :
        result= s[beginNum:endNum]
    return result

# 获取本机外网IP
def getInternetIP():
    r=requests.get(soipUrl,headers=headers)
    return lineLookup(r.text,'user_ip="','";')

def sendTheMsgToDingtalk(text):
    data={'msgtype':'markdown','markdown':{'title': dingtalkKeyword, 'text': text}}
    requests.post(dingtalkUrl, data=json.dumps(data), headers=headers)

# 日志分析类，目前支持Nginx日志和Uwsgi日志
class logsMsg():
    def __init__(self,logString):
        self.logString=logString
        self.ipList=self.getIpInList()
        self.api, self.requestTpye=self.getOrPostApi()
        self.timeStr=self.getTimeStr()
    def getIpInList(self):
        iplist=re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", self.logString)
        if iplist:
            return iplist
        else:
            return ['canNotFoundIp']
    def getOrPostApi(self):
        s=str(self.logString)
        if 'GET ' in s:
            api=lineLookup(s,'GET ',' ')
            requestTpye='GET'
        elif 'POST ' in s:
            api=lineLookup(s,'POST ',' ')
            requestTpye='POST'
        else:
            requestTpye,api ='canNotFoundGETorPOST',''
        return api,requestTpye
    def getTimeStr(self):
        # 不严谨时间提取法
        return lineLookup(self.logString,' [','] ')