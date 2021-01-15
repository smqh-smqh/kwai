#!/usr/bin/python
# -*- coding: UTF-8 -*-
import mitmproxy.http
from mitmproxy import ctx, http
import os
import json 
import atexit

update_flag = True
local_flag=False
# update_flag = False
# local_flag=True
filename='record.json'
dict={}

def w_file(contents):
    with open('record','w',encoding='utf-8') as wf:
        wf.write(contents)

def r_file():
    with open(filename,'r+',encoding='utf-8') as rf:
        content=rf.read()
    return content


def cancel_lunbo(dict):
    url="/rest/app/selection/feed"
    # print(dict[url]['body'][0]['bodyContents'])
    if dict[url]['body'][0]['title']=='轮播图' and len(dict[url]['body'][0]['bodyContents'])>1:
        for i in range(1,len(dict[url]['body'][0]['bodyContents'])):
            del dict[url]['body'][0]['bodyContents'][1]
            print(str(i)+"删除成功")
        print('轮播图取消成功')
        print(dict[url]['body'][0]['bodyContents'])


class Joker:

    def __init__(self):
        print("构造函数")
        if os.path.getsize(filename)>2:
            dict=json.loads(r_file())
            # cancel_lunbo(dict)
            self.dict=dict
            print(dict.keys())


    
    def response(self, flow: mitmproxy.http.HTTPFlow):
        
        interface_list=["/v3/regions","/v3/regions/new/63","/rest/app/selection/feed/singleColumn","/rest/app/selection/feed","/rest/app/abTest/config","/rest/app/flash/screen/list","/rest/app/search/recommend","/rest/app/search/recommend/resource"] #实际的接口

        url_path=flow.request.path.split('?')[0]
        if url_path in interface_list:
            ctx.log.warn('response来了')
            ctx.log.warn(url_path)
            if local_flag:
                # print(self.dict.get("/v3/regions"))
                flow.response.set_text(json.dumps(self.dict[url_path]))
                # ctx.log.warn(str(self.dict[url_path]['body'][0]['bodyContents']))
                # log中打印
                ctx.log.warn('response已更改')
            else:
                dict[url_path]=json.loads(flow.response.text)
                ctx.log.warn(url_path+'本地的response已更改')

    @atexit.register
    def clean():
        print('这是析构函数')       
        if update_flag:
            cancel_lunbo(dict)
            with open(filename, 'w') as f:
                json.dump(dict, f,ensure_ascii=False,indent=4)
            print("接口已更新")

addons = [
    Joker(),
]
    # def __del__(self):
    #     print('这是析构函数')
    #     if self.update_flag:
    #         print("析构函数已更新")
    #         self.w_file(self.dict)
            

    # def request(self, flow: mitmproxy.http.HTTPFlow):
        # if flag and os.path.exists(filename):
        #     flow.response.set_text(json.dumps({"result":"1001","message":"服务异常"}))
        # request_url=flow.request.path.split("?")[0]
        # if request_url=="https://apipc.app.acfun.cn/v3/regions" and dict.has_key(request_url):
        #     flow.response.set_text(json.dumps(self.dict[request_url]))

        
