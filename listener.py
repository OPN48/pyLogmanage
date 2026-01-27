from logTools.config import *
from logTools.tools import sendTheMsgToDingtalk, getText

# 初始化服务器报文 【x.x.x.x】:
text = headerText

if lastLinesNum:
    text+='The Last '+str(lastLinesNum)+' lines log:\n\n'
    # print(text)
else:
    text+='The all logs:\n\n'
defaultText = text
# 每秒监听
print(text,logFileList)
text=getText(text,logFileList,step=1)
# 无数据提升至每分钟监听
if defaultText == text:
    text = getText(text, logFileList, step=60)
    
if defaultText == text:
    text += 'Had not APIs more than ' + str(oneSecondMaxlog) + ' requests per second or minute'
# print(text)
if isDingtalkMsg:
    sendTheMsgToDingtalk(text=text)