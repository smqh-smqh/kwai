# --*-- coding: utf-8 --*--
# from urllib import request

import requests
from requests.packages import urllib3
import json
import time
from datetime import datetime
urllib3.disable_warnings()

url_201='https://cal.corp.kuaishou.com/e/calendar/meetingroom/scanCode/fcABC7Rl0G_109VffUMCNsKDa'
url_204='https://cal.corp.kuaishou.com/e/calendar/meetingroom/scanCode/fcADlilf7F6A58RAUOhZsxHzy'
url_205='https://cal.corp.kuaishou.com/e/calendar/meetingroom/scanCode/fcADktjRpmQcoofqkx0sZFbRX'
url1='https://home.corp.kuaishou.com/api/home/block?blockName=calendarStrokeViewDTO'
url_msg='https://is.corp.kuaishou.com/wx/message/send?access_token=ACE94AC400DAD05B82B375FA5CD59965'

header1={
'Cookie': 'accessproxy_session=1463632a-ab85-4886-bd9a-367ac1cbbdbd; k-token=89e3d52c8ca0089c278695faab422c79;'

}

header2={
'Cookie': '_did=web_894943991EC8551C; KXID=8kv0UjInJNsoW27gI4CvZJltTzNxYtTLtJIEPO25GBtPpTiRLa-RNj1ZyUr7lu9Pi44lAjT-sEXj-fNnqfgKNYpcUvRfnioSQhpFNwT-23UVCuzRoP7OpNzoLW8iqN_Y; accessproxy_session=7a6d06c1-f477-4218-b4c4-91b2feb763e5;'

}


def msg_send(content):
    body={
    "touser" : "wangyaxing03",
    "msgtype" : "text",
    "text" : {
    "content" : content
    },
    "safe":0
    }
    header_msg={
        'Content-Type':'application/json'

    }
    requests.post(url_msg,headers=header_msg,data=json.dumps(body),verify=False)
    
def job():  
    try:
        html=requests.get(url1,headers=header1,verify=False).text
        json_res = json.loads(html)
        # print(json_res)
        date_pattern = "%Y年%m月%d日%H:%M"
        mettings = json_res['calendarStrokeDetailViewDTOS']
        for m in mettings:
            # print(m['meetingDate'])
            if(m['spot'] is None):
                continue
            date=datetime.strptime(m['meetingDate']+m['beginTime'], date_pattern)
            if(0==datetime.now().day-date.day):
                if((datetime.now()-date).seconds<=600 or (datetime.now()-date).seconds>=86100):
                    # print((datetime.now()-date).seconds)
                    if('201' in m['spot']):
                        html=requests.get(url_201,headers=header2,verify=False).text
                        if(html.find("201 关雎")>0):
                            string=datetime.now().strftime(date_pattern)+' '+m['topic']+ m['spot']+'已签到'
                            print(string)
                            msg_send(string)
                        else:
                            try:
                                raise NameError("cookie过期")
                            except NameError:
                                msg_send('cookie过期')
                    elif('204' in m['spot']):
                        html=requests.get(url_204,headers=header2,verify=False).text
                        if(html.find("204 汉广")>0):
                            string=datetime.now().strftime(date_pattern)+' '+m['topic']+ m['spot']+'已签到'
                            print(string)
                            msg_send(string)
                        else:
                            try:
                                raise NameError("cookie过期")
                            except NameError:
                                msg_send('cookie过期')
                    elif('205' in m['spot']):
                        html=requests.get(url_205,headers=header2,verify=False).text
                        if(html.find("205 麟之")>0):
                            string=datetime.now().strftime(date_pattern)+' '+m['topic']+ m['spot']+'已签到'
                            print(string)
                            msg_send(string)
                        else:
                            try:
                                raise NameError("cookie过期")
                            except NameError:
                                msg_send('cookie过期')
                    else:
                        print('该会议室没有签到链接')
                else:
                    print(datetime.now().strftime(date_pattern)+' '+m['topic']+'暂时不用签到')
    
    except Exception:
        msg_send('cookie过期')


while True:
    job()
    time.sleep(300)