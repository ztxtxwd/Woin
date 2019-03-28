# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals

import sae.kvdb
import json
import requests
from ChineseAntiword import demo
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def fc(content):
    TAG_URL = 'http://api.bosonnlp.com/tag/analysis'
    # 如果某个选项采用默认设置，可以在TAG_URL中省略，完整的TAG_URL如下：
    # 'http://api.bosonnlp.com/tag/analysis?space_mode=0&oov_level=3&t2s=0&special_char_conv=0'
    # 修改space_mode选项为1
    # TAG_URL = \
    #   'http://api.bosonnlp.com/tag/analysis?space_mode=1'
    # 修改oov_level选项为1
    # TAG_URL = \
    #    'http://api.bosonnlp.com/tag/analysis?oov_level=1'
    # 修改t2s选项为1
    # TAG_URL= \
    #     'http://api.bosonnlp.com/tag/analysis?t2s=1'
    # 修改special_char_conv选项为1
    # TAG_URL= \
    # 'http://api.bosonnlp.com/tag/analysis?special_char_conv=1'
    
    s = [content]
    data = json.dumps(s)
    headers = {
        'X-Token': '1egi3t6g.32561.VBYvh3aBdKed',
        'Content-Type': 'application/json'
    }
    resp = requests.post(TAG_URL, headers=headers, data=data.encode('utf-8'))
    
    
    for d in resp.json():
        s=(' '.join(['%s' % it for it in zip(d['word'])]))
        pass
    words= s.split(" ")
    for i in range(0,len(words)):


        #更换获取反义词方式
    	# antiWord=demo(words[i])#这里
    	# if antiWord!='N':
    	# 	content=content.replace(words[i],antiWord)
    	# 	pass
    	
        kv=sae.kvdb.Client()
        antiWord=str(kv.get(words[i].encode("utf-8")))
        print(words[i])
        if antiWord!='None':
            content=content.replace(words[i],antiWord)
            pass

        pass
    pass
    return content
