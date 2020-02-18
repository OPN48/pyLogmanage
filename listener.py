from logTools.config import *
from logTools.tools import getIpInStr

for f in logFileList:
    logFile=open(f,'r')
    l=logFile.readlines()[-100:]
    for line in l:
        ip=getIpInStr(line)
        print(line)
        print(ip)
    logFile.close()
