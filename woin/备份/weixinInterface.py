# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import fenci
import sae.kvdb
import oppose
import sys
from lxml import etree

class WeixinInterface:

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr = data.echostr
        #自己的token
        token="token" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
	
    def POST(self): 
        kv=sae.kvdb.Client()
        str_xml = web.data()
        xml = etree.fromstring(str_xml)
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text 
        toUser=xml.find("ToUserName").text 
        if msgType == 'text':
            content=xml.find("Content").text
            opposingUsers=kv.get("isOpposing")
            if 'reset' in content:
                kv.delete('isOpposing')
                kv.delete('lastTalk_dict')
                kv.delete('dirtyTalk_dict')
                kv.add('isOpposing','u1 ',min_compress_len=0)
                kv.add('lastTalk_dict',"{'nmsl': 'nmsl'}",min_compress_len=0)
                dt=u'傻逼'
                #kv.add('dirtyTalk_dict',"{'"+dt+"':'"+dt+"'}",min_compress_len=0)
                kv.add('dirtyTalk_dict',"{'nmsl':'nmsl'}",min_compress_len=0)
                pass
            elif fromUser in opposingUsers:
                content=oppose.getResponse(fromUser,content)
                kv.get('lastTalk_dict')
                pass
            elif u'作对' in content:
                opposingUsers+=fromUser+' '
                kv.set('isOpposing',opposingUsers)
                content=u'作对模式消息粗鄙污秽不堪，脏话敏感者慎用，未成年人请在监护人陪同下使用。回复：“我就是个弟弟”退出作对模式。跟我作对指定没你好果子吃的弟弟，$NMSL'
                oppose.startOppose(fromUser)
                pass
            else:
                content=fenci.fc(content)
            # if '哥我错了' in content:
            #     isOpposingList=kv.get('isOpposing')
            #     newList=isOpposingList.split(' ').remove(fromUser)
            #     kv.set('isOpposing',' '.join(newList))
            #     content='知错就改还是好妹妹'
            #     pass
            # elif '作对' in content:
            #     isOpposingList=kv.get('isOpposing')
            #     isOpposingList+=fromUser+' '
            #     kv.set('isOpposing',isOpposingList)
            #     content='臭弟弟，NMSL'
            #     ast.literal_eval(kv.get('lastTalk_dict'))[fromUser]=content
            #     pass
            # elif '作对' in kv.get(fromUser):
            #     content=oppose.getResponse(fromUser,content)#作对模式
            #     print('zuoduimoshi')
            #     pass
            # else:
            #     content=fenci.fc(content)
            
            # print(kv.get(fromUser))
            kv.disconnect_all()
            return self.render.reply_text(fromUser,toUser,int(time.time()),content)
        elif msgType == 'image':
            return self.render.reply_text(fromUser,toUser,int(time.time()), "mei")
            pass
        else:
            pass