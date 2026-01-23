import json
from logTools.config import *
from logTools.tools import getSysArgv

safeKeys=modelDic.keys()
keyReplace=dict(zip([modelDic[i][0] for i in modelDic],list(safeKeys)))

def getInternetIP():
    for api in IP_APIS:
        try:
            response = requests.get(api, timeout=5)
            if response.status_code == 200:
                public_ip = response.text.strip()
                if 'origin' in public_ip:
                    public_ip = json.loads(public_ip)['origin']
                return public_ip
        except requests.exceptions.RequestException as e:
            # 单个API失败时，打印提示并尝试下一个
            print(f"ip API {api} false: {e}")
            continue
    return IP_DEFAULT_NAME

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
    if os.path.exists(CONFIG_FILENAME):
        f = open(CONFIG_FILENAME, 'r')
        for line in f:
            if line.strip():
                key, value = line.split(' ', 1)
                tempDic[key] = value.strip()
    print(f'此前配置{tempDic}')
    print(f'输入配置{inputDic}')
    inputDic.get('ip', IP_DEFAULT_NAME)
    inputDic=tempDic|inputDic
    # 初始化服务器外网ip
    if inputDic.get('ip', IP_DEFAULT_NAME) == IP_DEFAULT_NAME:
        inputDic['ip'] = getInternetIP()

    print(f'合并后配置{inputDic}')
    f = open(CONFIG_FILENAME, 'w')
    for key in inputDic:
        if key:
            f.write(key + ' ' + inputDic[key]+'\n')
            print('配置 %s 成功，配置值为：%s'%(key,inputDic[key]))
    f.close()