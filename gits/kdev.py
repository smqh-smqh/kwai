import json
import re

# #########填充FM TC############
# 1.在test_mind.json中粘贴数据库内容
# 2.python3 kdev.py
# 3.在1.json里粘贴content字段复制到数据库

_id=''
mindId=''
def read_file(filepath):
    with open(filepath) as fp:
        content=fp.read()
        pattern = re.compile(r'(ObjectId\("(.*)"\))')   # 查找数字
        result1 = pattern.findall(content)
        global _id
        _id=result1[0][0]
        global mindId
        mindId=result1[1][0]
        # print(_id+"  "+mindId)
        news1='"'+'ObjectId('+result1[0][1]+')'+'"'
        news2='"'+'ObjectId('+result1[1][1]+')'+'"'
        content=content.replace(result1[0][0],news1).replace(result1[1][0],news1)
    return content


def rule(context):
    try:
        if context['children']!=[]:
            context['data']['text']="FM:"+context['data']['text']
            # print(context['data']['text'])
            for item in context['children']:
                rule(item)
        else:
            context['data']['text']="TC:"+context['data']['text']
            # print(context['data']['text'])
        if 'imageSize' in context['data'] and context['data']['imageSize']=="":
            del context['data']['imageSize']
    except:
        # print(context)
        return


ret=read_file('test_mind.json')
ret=json.loads(ret)
context=ret['content']['root']
for item in context['children']:
    rule(item)
ret['content']['root']=context
ret['_id']=_id
ret['mindId']=mindId
print(ret['_id']+' '+ret['mindId'])
with open("1.json","w") as f:
    json.dump(ret,f,ensure_ascii=False,indent=4)