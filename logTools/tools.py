import re,json,datetime,time

from logTools.config import *

def getSysArgv(keyReplace, safeKeys):
    inputDic={}
    import sys
    l=sys.argv
    if l[1:]==[] or '-h'==l[1] or '-help'==l[1]:
        pass
    else:
        for item in l:
            if '-'==item[0]:
                num=l.index(item)
                if num+1<len(l):
                    if '-'!=l[num+1][0]:
                        inputDic[item[1:]]=l[num+1]
    outputDic={}
    for key in inputDic:
        if key in keyReplace:
            outputDic[keyReplace[key]]=inputDic[key]
        if key in safeKeys:
            outputDic[key]=inputDic[key]
    return outputDic



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
    data={'msgtype':'markdown','markdown':{'title': dkeyword, 'text': text}}
    requests.post(durl, data=json.dumps(data), headers=headers)

# 日志分析类，目前支持Nginx日志和Uwsgi日志
class logsMsg():
    def __init__(self,logString):
        self.logString=logString
        self.ipList=self.getIpInList()
        self.api, self.requestTpye=self.getOrPostApi()
        self.datetimeStr,self.datetime,self.mktime=self.getTimeStr()

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
        monthDic={'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        replaceStr='/-:'
        logStr=str(self.logString)
        for m in monthDic:
            if m in logStr:
                logStr=logStr.replace(m,monthDic[m])
        patternList=[
            # Nginx error log: 2020/02/21 00:20:28 [error]
            ('\d{4}[-/]\d{1,2}[-/]\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}',('year','month','day','hour','minute','second')),
            # Nginx access log:[21/Feb/2020:16:45:28 +0800] 210
            ('\d{1,2}[-/]\d{1,2}[-/]\d{4}:\d{1,2}:\d{1,2}:\d{1,2}',('day','month','year','hour','minute','second')),
            # uWSGI log:Wed Feb 19 06:13:47 2020 or Wed Feb  9 06:13:47 2020
            ('\d{1,2}\s+\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\s\d{4}',('month','day','hour','minute','second','year'))
        ]
        datetimeStr = 'canNotFindTime'
        datetimeDic = {'error': 'canNotFindTime'}
        for pattern in patternList:
            timeList = re.findall(pattern[0], logStr)
            if timeList:
                datetimeStr = timeList[0]
                for s in replaceStr:
                    datetimeStr=datetimeStr.replace(s,' ')
                datetimeStr=datetimeStr.replace('  ',' ')
                datetimeDic=dict(zip(pattern[1], datetimeStr.split(' ')))
                datetimeStr=' '.join([datetimeDic[key] for key in ('year','month','day','hour','minute','second')])
                break
        try:
            for i in ('year','month','day','hour','minute','second'):
                datetimeDic[i]=int(datetimeDic[i])
            d=datetime.datetime(**datetimeDic)
            return datetimeStr,d,int(time.mktime(d.timetuple()))
        except:
            print(logStr)
            return datetimeStr, datetime.datetime(1970,1,1,8,0,0), 0


def getText(text,logFileList,step=1):
    # 日志分析
    tempDic = {}
    for f in logFileList:
        logFile = open(f, 'r')
        l = logFile.readlines()[-lastLinesNum:]
        dic = {}
        for line in l:
            log = logsMsg(line)
            projectName = f.split(fileNameDelimiter)[0]
            timeIpApiStr = str(str(int(log.mktime/step))+ delimiter + log.ipList[0] + delimiter + projectName + log.api)
            if timeIpApiStr in dic:
                # 识别不到api时不加一
                if log.api != '':
                    dic[timeIpApiStr] += 1
                else:
                    pass
            else:
                dic[timeIpApiStr] = 1
        logFile.close()
        for key in dic:
            count = dic[key]
            if count >= oneSecondMaxlog:
                stepNum = (count // oneSecondMaxlog) * oneSecondMaxlog
                if stepNum in tempDic:
                    tempDic[stepNum].append(key)
                else:
                    tempDic[stepNum] = [key]
    for count in tempDic:
        text += '【more than ' + str(count) + '/%ss】:\n\n'% step
        tempList = []
        for s in tempDic[count]:
            api = s.split(delimiter)[-1]
            if api not in tempList:
                tempList.append(api)
        text += '\n\n'.join(tempList) + '\n\n'
    return text