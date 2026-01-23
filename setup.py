import os
from logTools.config import modelDic, CONFIGFILENAME, isDingtalkMsg, durl
from logTools.tools import getSysArgv

safeKeys=modelDic.keys()
keyReplace=dict(zip([modelDic[i][0] for i in modelDic],list(safeKeys)))

helpStr='用法: python3 setup.py [-options] [args...](执行初始化配置)\n'
for key in modelDic:
    shortKey = modelDic[key][0]
    msg = modelDic[key][1]
    default = modelDic[key][2]
    helpStr += '    -%s -%s    \t%s 默认:%s\n'%(shortKey,key,msg,default)

inputDic = getSysArgv(keyReplace, safeKeys)

if not inputDic:
    print(helpStr)
else:
    tempDic = {}
    if os.path.exists(CONFIGFILENAME):
        f = open(CONFIGFILENAME, 'r')
        for line in f:
            if line.strip():
                key, value = line.split(' ', 1)
                tempDic[key] = value.strip()
    print(f'此前配置{tempDic}')
    print(f'输入配置{inputDic}')
    inputDic=tempDic|inputDic
    print(f'合并后配置{inputDic}')
    f = open(CONFIGFILENAME, 'w')
    for key in inputDic:
        if key:
            f.write(key + ' ' + inputDic[key]+'\n')
            print('配置 %s 成功，配置值为：%s'%(key,inputDic[key]))
    f.close()