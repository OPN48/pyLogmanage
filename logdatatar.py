import datetime
from logTools.config import *
from logTools.tools import getInternetIP, getFileSize, sendTheMsgToDingtalk

# 初始化服务器报文 【x.x.x.x】:
text = '【%s】：\n\n' % getInternetIP()

# 昨天日期文件名
today = datetime.date.today()
yesterdayFileName = 'log-' + str(today - datetime.timedelta(days=1)) + '.tar.gz'
# 删除日期文件名
deleteFileName = 'log-' + str(today - datetime.timedelta(days=deleteDays)) + '.tar.gz'

# 获取文件名及文件大小
for f in logFileList:
    fileSize = getFileSize('./' + f)
    if fileSize >= warnsize:
        text += '【文件过大】'
    text += str(f) + ' ' + str(fileSize) + 'MB \n\n'

# 压缩日志
try:
    os.system('tar -czvf ./%s %s' % (yesterdayFileName, ' '.join(logFileList)))
    tarSize = str(getFileSize('./' + yesterdayFileName))
    text += yesterdayFileName + ' ' + tarSize + 'MB \n\n'
except:
    print('tar error, please check you fileType config')

# 删除所有log,重新创建文件
os.system('rm -rf ./*%s && touch %s' % (fileType, ' '.join(logFileList)))

# 删除过期日志压缩包
if os.path.exists('./' + deleteFileName):
    os.system('rm -rf ./' + deleteFileName)
    # 报文增加删除文件
    text += '删除文件有：' + deleteFileName + '\n\n'
else:
    pass

# 告知nginx重读日志文件
if isNginx:
    os.system('nginx -s reopen')
# 告知UWSGI重写日志
if isUwsgi:
    uwsgiLogrotate = logFilePath + '/touchforlog'
    os.system('touch ' + uwsgiLogrotate)
# 增加服务器剩余空间告警
df = os.popen('df -lh').read().strip().split('\n')
for l in df:
    if l[-1] in '/':
        text += l + '\n\n'

# 发送消息给钉钉
if isDingtalkMsg:
    sendTheMsgToDingtalk(text=text)
