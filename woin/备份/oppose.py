# -*- coding: utf-8 -* 
import sae.kvdb
import ast
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')

def getResponse(userId,content):
    args=before()
    isOpposing_list=args[0].split(" ")#The special parameter, type is list
    
    lastTalk_dict=ast.literal_eval(args[1])
    
    dirtyTalk_dict=ast.literal_eval(args[2])



    if '我就是个弟弟' in content:
        
        isOpposing_list.remove(userId)
        args[0]=" ".join(isOpposing_list)
        after(args)
        return u'您配吗？'
        pass


    else:

        #1.存：在kv.lastTalk_dict中找到服务器向此用户发送的上一句话lastTalk，
        lastTalk=lastTalk_dict[userId]
        #通过lastTalk在dirtyTalk_dict中将content存入lastTalk:[content]
        keys=dirtyTalk_dict.keys()
        if lastTalk not in keys:
            dirtyTalk_dict[lastTalk]=content
            args[2]=str(dirtyTalk_dict)
            pass
        else:
            responses=dirtyTalk_dict[lastTalk]
            if content not in responses.split(","):
                responses+=","+content
                pass
            dirtyTalk_dict[lastTalk]=responses
            args[2]=str(dirtyTalk_dict)
            pass
        mostLike=process.extractOne(content,keys,scorer=fuzz.UWRatio)[0]
        print(dirtyTalk_dict[mostLike].split(','))
        resp=random.sample(dirtyTalk_dict[mostLike].split(','),1)[0]

        lastTalk_dict[userId]=resp
        args[1]=str(lastTalk_dict)
        after(args)
        return resp
def startOppose(userId):
    args=before()
    lastTalk_dict=ast.literal_eval(args[2])
    lastTalk_dict[userId]=u'与我作对指定没你好果汁吃'
    args[1]=str(lastTalk_dict)
    after(args)
    pass


def before():
    kv=sae.kvdb.Client()
    isOpposing=kv.get('isOpposing')#字符串类型，格式："u1 u2 u3 ..."
    lastTalk=kv.get('lastTalk_dict')#字符串型，dict形式
    dirtyTalk=kv.get('dirtyTalk_dict')#字符串型，dict形式
    kv.disconnect_all()
    return [isOpposing,lastTalk,dirtyTalk]
    pass

def after(args):
    kv=sae.kvdb.Client()
    kv.set('isOpposing',args[0])
    kv.set('lastTalk_dict',args[1])
    kv.set('dirtyTalk_dict',args[2])
    kv.disconnect_all()
    print('isOpposing:'+args[0])
    print('lastTalk_dict:'+args[1])
    print('dirtyTalk_dict'+args[2])
    pass