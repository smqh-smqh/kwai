import mitmproxy.http
from mitmproxy import ctx
import json

def response(flow: mitmproxy.http.HTTPFlow):
    if flow.request.path.startswith("/rest/app/abTest/config"):
            # #返回数据json，绝对路径
            # with open('/Users/wyx/Desktop/slideList','rb') as f:
            #     res = json.load(f)
            # #设置返回数据
            # flow.response.set_text(json.dumps(res))
            # #log中打印
            # ctx.log.info('哈哈哈')
            string=flow.response.get_text()
            ctx.log.info(string)
            res=json.loads(string)
            res["config"]['returnLayerNumber']="1"
            flow.response.set_text(json.dumps(res))
            ctx.log.info('哈哈哈')
            # for item in res['feed']:
            #     ctx.log.info(item['meow']['createTime'])

    