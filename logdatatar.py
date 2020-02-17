import datetime,os,json,requests
from logTools.config import *

# 获取本机外网IP
def getInternetIP(headers=headers):
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

# 初始化服务器报文 【x.x.x.x】:
text='【%s】：\n\n' % getInternetIP()

nowPath=os.getcwd()
logFileList=list(filter(None, [f if os.path.splitext(f)[1] == fileType else '' for f in os.listdir(nowPath)]))

# 昨天日期文件名
today=datetime.date.today()
yesterdayFileName= 'log-' + str(today - datetime.timedelta(days=1))+'.tar.gz'
# 删除日期文件名
deleteFileName= 'log-' + str(today - datetime.timedelta(days=deleteDays))+'.tar.gz'

# 获取文件名及文件大小
for f in logFileList:
    text+=str(f)+' '+str(getFileSize('./'+f))+'MB \n\n'

# 压缩日志
os.system('tar -czvf ./%s %s' % (yesterdayFileName, ' '.join(logFileList)))
tarSize=str(getFileSize('./'+yesterdayFileName))
text+=yesterdayFileName+' '+tarSize+'MB \n\n'

# 删除所有log,重新创建文件
os.system('rm -rf ./*%s && touch %s'%(fileType,' '.join(logFileList)))

# 删除过期日志压缩包
if os.path.exists('./' + deleteFileName):
    os.system('rm -rf ./' + deleteFileName)
    # 报文增加删除文件
    text+='删除文件有：'+deleteFileName
else:
    pass

# 告知nginx重读日志文件
if isNginx:
    os.system('nginx -s reopen')
# 告知UWSGI重写日志
if isUwsgi:
    os.system('touch ' + uwsgiLogrotate)

# 发送消息给钉钉
if isDingdingMsg:
    data={'msgtype':'markdown','markdown':{'title': dingdingKeyword, 'text': text}}
    s = json.dumps(data)
    requests.post(dingdingUrl, data=s, headers=headers)