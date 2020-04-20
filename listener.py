from logTools.config import *
from logTools.tools import sendTheMsgToDingtalk, getInternetIP, getText

text='【%s】' % getInternetIP()
if lastLinesNum:
    text+='The Last '+str(lastLinesNum)+' lines log:\n\n'
else:
    text+='The all logs:\n\n'
defaultText = text
# 每秒监听
text=getText(text,logFileList,step=1)
# 无数据提升至每分钟监听
if defaultText == text:
    text = getText(text, logFileList, step=60)
    
if defaultText == text:
    text += 'Had not APIs more than ' + str(oneSecondMaxlog) + ' requests per second or minute'

if isDingtalkMsg:
    print(text)
    # sendTheMsgToDingtalk(text=text)