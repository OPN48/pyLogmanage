from logTools.config import *
from logTools.tools import logsMsg, sendTheMsgToDingtalk, getInternetIP

text='【%s】' % getInternetIP()
if lastLinesNum:
    text+='The Last '+str(lastLinesNum)+' lines log:\n\n'
else:
    text+='The all logs:\n\n'
defaultText=text
# 日志分析
tempDic = {}
for f in logFileList:
    logFile=open(f,'r')
    l=logFile.readlines()[-lastLinesNum:]
    dic = {}
    for line in l:
        log=logsMsg(line)
        projectName=f.split('_')[0]
        timeIpApiStr=str(log.datetimeStr.replace(' ','') + '_' + log.ipList[0] + '_' + projectName + log.api)

        if timeIpApiStr in dic:
            # 识别不到api时不加一
            if log.api!='':
                dic[timeIpApiStr] += 1
            else:
                pass
        else:
            dic[timeIpApiStr]=1
    logFile.close()
    for key in dic:
        if dic[key] >= oneSecondMaxlog:
            stepNum= (dic[key] // oneSecondMaxlog) * oneSecondMaxlog
            if stepNum in tempDic:
                tempDic[stepNum].append(key)
            else:
                tempDic[stepNum]=[key]

for count in tempDic:
    text+='【more than '+str(count)+'/s】:\n\n'
    tempList=[]
    for s in tempDic[count]:
        api=s.split('_')[-1]
        if api not in tempList:
            tempList.append(api)
    text += '\n\n'.join(tempList) +'\n\n'
    tempList = []

if defaultText == text:
    text += 'Had not APIs more than ' + str(oneSecondMaxlog) + ' requests per second'

if isDingtalkMsg:
    sendTheMsgToDingtalk(text=text)