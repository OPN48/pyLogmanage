from logTools.tools import getSysArgv

default={
    'dingtalkUrl':''
    # 'dingtalkKeyword':'logdatatar'
}
inputDic=getSysArgv(defaultDic=default)
if inputDic['dingtalkUrl']!='':
    f=open('./dingtalkUrl','w')
    f.write('dingtalkUrl '+inputDic['dingtalkUrl'])
    f.close()
else:
    print('please input your dingtalk robot url')