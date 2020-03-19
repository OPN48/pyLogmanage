from logTools.config import *
from logTools.tools import logsMsg, sendTheMsgToDingtalk, getInternetIP, getText

text='【%s】' % getInternetIP()
if lastLinesNum:
    text+='The Last '+str(lastLinesNum)+' lines log:\n\n'
else:
    text+='The all logs:\n\n'
defaultText = text
text=getText(text,logFileList,step=1)

if defaultText == text:
    # text += 'Had not APIs more than ' + str(oneSecondMaxlog) + ' requests per second'
    text = getText(text, logFileList, step=60)

if isDingtalkMsg:
    sendTheMsgToDingtalk(text=text)