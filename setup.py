from logTools.config import modelDic, configFileName, isDingtalkMsg, durl
from logTools.tools import getSysArgv

safeKeys=modelDic.keys()
keyReplace=dict(zip([modelDic[i][0] for i in modelDic],list(safeKeys)))

helpStr='用法: python3 setup.py [-options] [args...](执行初始化配置)\n'
for key in modelDic:
    shortKey=modelDic[key][0]
    msg=modelDic[key][1]
    default=modelDic[key][2]
    helpStr += '    -%s -%s    \t%s 默认:%s\n'%(shortKey,key,msg,default)

inputDic=getSysArgv(keyReplace, safeKeys)

if not inputDic:
    print(helpStr)
else:
    f = open(configFileName, 'w')
    for key in inputDic:
        f.write(key + ' ' + inputDic[key])
        print('配置 %s 成功，配置值为：%s'%(key,inputDic[key]))
    f.close()