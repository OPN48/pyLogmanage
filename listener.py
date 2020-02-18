from logTools.config import *
from logTools.tools import logsMsg, sendTheMsgToDingtalk

if lastLinesNum:
    text='The Last '+str(lastLinesNum)+' lines log:\n\n'
else:
    text='The all logs:\n\n'

for f in logFileList:
    logFile=open(f,'r')
    l=logFile.readlines()[-lastLinesNum:]
    dic = {}
    for line in l:
        log=logsMsg(line)
        timeIpApiStr=str(log.timeStr+' '+log.ipList[0]+' '+log.api)
        if timeIpApiStr in dic:
            dic[timeIpApiStr] += 1
        else:
            dic[timeIpApiStr]=1
    logFile.close()
    # 日志分析
    tempText=''
    tempDic={}
    for key in dic:
        if dic[key] >=oneMinMaxlog:
            if dic[key] in tempDic:
                tempDic[dic[key]].append(key)
            else:
                tempDic[dic[key]]=[key]
    for count in tempDic:
        text+='The APIs more than '+str(count)+' requests per minute:\n\n'
        for s in tempDic[count]:
            api=s.split(' ')[-1]
            text += api +'\n\n'

if isDingtalkMsg:
    sendTheMsgToDingtalk(text=text)