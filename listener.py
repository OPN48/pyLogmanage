from logTools.config import *
from logTools.tools import logsMsg, sendTheMsgToDingtalk, getInternetIP

text='【%s】' % getInternetIP()
if lastLinesNum:
    text='The Last '+str(lastLinesNum)+' lines log:\n\n'
else:
    text='The all logs:\n\n'
defauleText=text
# 日志分析
tempDic = {}
for f in logFileList:
    logFile=open(f,'r')
    l=logFile.readlines()[-lastLinesNum:]
    dic = {}
    for line in l:
        log=logsMsg(line)
        projectNmae=f.split('_')[0]
        timeIpApiStr=str(log.timeStr+' '+log.ipList[0]+' '+projectNmae+log.api)
        if timeIpApiStr in dic:
            dic[timeIpApiStr] += 1
        else:
            dic[timeIpApiStr]=1
    logFile.close()
    for key in dic:
        if dic[key] >= oneMinMaxlog:
            stepNum=(dic[key]//oneMinMaxlog)*oneMinMaxlog
            if stepNum in tempDic:
                tempDic[stepNum].append(key)
            else:
                tempDic[stepNum]=[key]

for count in tempDic:
    text+='The APIs more than '+str(count)+' requests per minute:\n\n'
    tempList=[]
    for s in tempDic[count]:
        api=s.split(' ')[-1]
        if api not in tempList:
            tempList.append(api)
    text += '\n\n'.join(tempList) +'\n\n'
    tempList = []

if defauleText == text:
    text+='Had not APIs more than '+str(oneMinMaxlog)+' requests per minute'
    
# print(text)
if isDingtalkMsg:
    sendTheMsgToDingtalk(text=text)