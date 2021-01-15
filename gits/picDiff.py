# -*- encoding=utf8 -*-
__author__ = "nanganglei"

import time
from airtest.core.api import *
from poco.drivers.ios import iosPoco
from airtest.cli.parser import cli_setup
from on_off_diff import *

# ST.SNAPSHOT_QUALITY = 75

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=[
            "ios:///http://127.0.0.1:8100",
    ])


# script content
print("start...")
poco = iosPoco()
ONLINE_APP_NAME  = 'tv.acfun.lite'
OFFLINE_APP_NAME = 'com.kwai.xfunios.beta'
# ONLINE_APP_NAME='tv.danmaku.bilianime'
width, height = poco.get_screen_size() # 屏幕尺寸
curDir = os.getcwd()


def getCurrentTime():
    timeTemp = time.time()
    timeTempNext = time.localtime(timeTemp)
    timeNow = time.strftime("%Y-%m-%d", timeTempNext)   #转化为当前时间
    return timeNow

def appMineScreenshot(dir):
    sleep(2)
    poco("我的").click()
    snapshot(filename= dir + "myBar.jpg")

    # 设置页面截图
    poco("setting icon").click() # 设置页面
    sleep(2)
    snapshot(filename= dir+"setting.jpg")
    poco("谁可以私信我").click()
    snapshot(filename=dir+"msgSetting.jpg",msg="谁可以私信我截图")
    poco("ac navigationbar back white").click() # 返回到上一页面
    poco("关于我们").click()
    snapshot(filename=dir+"aboutusOnline.jpg",msg="关于我们截图")
    poco("ac navigationbar back white").click() # 返回到上一页面
    poco("反馈帮助").click()
    sleep(2)
    snapshot(filename=dir+"helpOnline.jpg",msg="反馈帮助截图")
    poco("我的反馈").click()
    sleep(2)
    snapshot(filename=dir+"myfeedback.jpg",msg="我的反馈截图")
    poco("ac navigationbar back white").click() # 返回到上一页面
    poco("编辑资料").click()
    snapshot(filename=dir+"editMe.jpg",msg="编辑资料截图")
    poco("ac navigationbar back white").click() # 返回到上一页面
    poco("ac navigationbar back white").click() # 返回到'我的'



    # 喜欢、帖子tab、粉丝列表、关注列表、查看头像截图
    touch(Template(r"tpl1600935271773.png", record_pos=(-0.105, -0.01), resolution=(1242.0, 2208.0)))
    snapshot(filename=dir+"myLikes.jpg")
    touch(Template(r"tpl1602744471397.png", record_pos=(0.146, -0.105), resolution=(1125, 2436)))

    snapshot(filename=dir+"myPost.jpg")

    poco(nameMatches=".*关注$").click() # 进入到关注列表
    sleep(2)
    snapshot(filename=dir+"myFollowing.jpg",msg="我的关注截图")

    swipe((width-10,height/2),(width/2,height/2),duration=1,steps=1) # 侧滑进入到粉丝列表
    sleep(2)
    snapshot(filename=dir+"myFollowed.jpg")
    poco("ac navigationbar back white").click() # 返回到上一页面
    poco(nameMatches=".*点赞$").click()
    snapshot(filename=dir+"likedCount.jpg",msg="点赞数")
    sleep(3)



    ## 消息通知
    poco("消息").click()
    snapshot(filename=dir+"message.jpg")
    
    poco("评论").click()
    sleep(2)
    snapshot(filename=dir+"messageComment.jpg")
    poco("ac navigationbar back white").click()
    
    poco("赞").click()
    sleep(2)
    snapshot(filename=dir+"messageLiked.jpg")
    poco("ac navigationbar back white").click()
    
    poco("系统通知").click()
    sleep(2)
    snapshot(filename=dir + "messageSystem.jpg")
    poco("ac navigationbar back white").click()
    # 转换成相对坐标
    x1 = 410/width
    y1 = 720/height
    poco.click([x1,y1])
    snapshot(filename=dir + "iM.jpg")
    poco("ac navigationbar back white").click()
    
    ## 卡劵
    poco("卡券").click()
    snapshot(filename=dir+"card.jpg")
    poco("获得记录").click()
    sleep(2)
    snapshot(filename=dir+"getHistory.jpg")
    poco("消耗记录").click()
    sleep(2)
    snapshot(filename=dir+"consumeHistory.jpg")
    poco("ac navigationbar back normal").click()
    
    ## 任务中心
    poco("任务中心").click()
    snapshot(filename=dir+"tasks.jpg")
    poco("去完成").click()
    sleep(2)
    snapshot(filename=dir+"gotoFinish.jpg")
    poco("ac navigationbar back white").click()
    poco("ac navigationbar back white").click()
    
    
    ## 历史记录
    poco("历史记录").click()
    snapshot(filename=dir+"history.jpg")
    poco.click([x1,y1])
    snapshot(filename=dir+"historyDetail.jpg")
    poco("ac navigationbar back white").click()
    poco("ac navigationbar back white").click()
    
    poco("我的订阅").click()
    sleep(1)
    snapshot(filename=dir+"mysubscribe.jpg")
    poco("ac navigationbar back white").click()
   
def appThemeScreenshot(dir):
    sleep(2)
    poco("剧场").click()
#     poco("推荐").click()
    snapshot(filename= dir + "themeBar.jpg")
    poco("排行榜").click()
    sleep(2)
    snapshot(filename= dir + "list.jpg")
    touch(Template(r"tpl1596597737906.png", record_pos=(-0.163, -0.531), resolution=(1125, 2436)))
    sleep(2)
    snapshot(filename= dir + "animeList.jpg")
    touch(Template(r"tpl1596597753724.png", record_pos=(0.04, -0.531), resolution=(1125, 2436)))
    sleep(2)
    snapshot(filename= dir + "comicList.jpg")
    poco("ac navigationbar back white").click()
    touch(Template(r"tpl1596597970263.png", record_pos=(-0.386, -0.768), resolution=(1125, 2436)))
    sleep(2)
    snapshot(filename= dir + "subsketch.jpg")
    touch(Template(r"tpl1596596334749.png", record_pos=(-0.128, -0.613), resolution=(1125, 2436)))
    sleep(2)
    snapshot(filename= dir + "subscomic.jpg")
    touch(Template(r"tpl1606119235075.png", record_pos=(0.094, -0.626), resolution=(1125, 2436)))


    sleep(2)
    snapshot(filename= dir + "subsanime.jpg")

    touch(Template(r"tpl1604375196119.png", record_pos=(0.109, -0.806), resolution=(828, 1792)))    
    sleep(2)

    snapshot(filename= dir + "sketch.jpg")
    poco("全部").click()
    sleep(2)
    snapshot(filename= dir + "sketchAll.jpg")
    poco("恋爱").click()
    sleep(2)
    snapshot(filename= dir + "sketchLove.jpg")
    poco("古风").click()
    sleep(2)
    snapshot(filename= dir + "sketchAntique.jpg")
    poco("穿越").click()
    sleep(2)
    snapshot(filename= dir + "sketchThrough.jpg")
    swipe(Template(r"tpl1596596926879.png", record_pos=(0.347, -0.624), resolution=(1125.0, 2436.0)), vector=[-0.2197, 0.0])
    poco("都市").click()
    sleep(2)
    snapshot(filename= dir + "sketchCity.jpg")
    poco("校园").click()
    sleep(2)
    snapshot(filename= dir + "sketchSchool.jpg")
    poco("热血").click()
    sleep(2)
    snapshot(filename= dir + "sketchBlood.jpg")

    
    
    touch(Template(r"tpl1596598101300.png", record_pos=(-0.004, -0.77), resolution=(1125, 2436)))
    sleep(2)

    snapshot(filename= dir + "anime.jpg")
    poco("全部").click()
    sleep(2)
    snapshot(filename= dir + "animeAll.jpg")
    poco("国漫").click()
    sleep(2)
    snapshot(filename= dir + "animeChina.jpg")
    poco("日漫").click()
    sleep(2)
    snapshot(filename= dir + "animeJanpa.jpg")
    poco("美漫").click()
    sleep(2)
    snapshot(filename= dir + "animeAmerica.jpg")
    touch(Template(r"tpl1606120932599.png", record_pos=(0.358, -0.777), resolution=(1125, 2436)))


    sleep(2)

    snapshot(filename= dir + "comic.jpg")
    poco("全部").click()
    sleep(2)
    snapshot(filename= dir + "comicAll.jpg")
    poco("恋爱").click()
    sleep(2)
    snapshot(filename= dir + "comicLove.jpg")
    poco("古风").click()
    sleep(2)
    snapshot(filename= dir + "comicAntique.jpg")
    poco("穿越").click()
    sleep(2)
    snapshot(filename= dir + "comicThrough.jpg")

    
def appSearchScreenshot(dir):
    sleep(1)
    touch(Template(r"tpl1604376211455.png", record_pos=(-0.391, -0.923), resolution=(828, 1792)))
    swipe((width/2,height-10),(width/2,height/2),duration=1,steps=1)

    text("1st")
    sleep(2)
    snapshot(filename= dir + "seachabc.jpg")
    poco("取消").click()


def appNoticeScreenshot(dir):
    sleep(1)
    poco("动态").click()
    sleep(2)
    snapshot(filename= dir + "focus.jpg")
    touch(Template(r"tpl1604376239748.png", record_pos=(-0.396, -0.932), resolution=(828, 1792)))


    sleep(2)
    snapshot(filename= dir + "find.jpg")



onlineDir   = curDir + '/pics/picsOnline_%s/'%(getCurrentTime())
offlineDir  = curDir + '/pics/picsOffline_%s/'%(getCurrentTime())
comparedDir = curDir + '/pics/picsCompared_%s/'%(getCurrentTime())
three_in_oneDir = curDir + '/pics/picsThree_in_one_%s/'%(getCurrentTime())
if not os.path.exists(onlineDir):
    os.makedirs(onlineDir)
if not os.path.exists(offlineDir):
    os.makedirs(offlineDir)
if not os.path.exists(comparedDir):
    os.makedirs(comparedDir)
if not os.path.exists(three_in_oneDir):
    os.makedirs(three_in_oneDir)
    
# print(getCurrentTime())
# print(onlineDir)
# 线上包截图
stop_app(ONLINE_APP_NAME)
# sleep(1)
start_app(ONLINE_APP_NAME)
appThemeScreenshot(onlineDir)
appSearchScreenshot(onlineDir)
appNoticeScreenshot(onlineDir)
appMineScreenshot(onlineDir)
stop_app(ONLINE_APP_NAME)

#测试包截图
stop_app(OFFLINE_APP_NAME)
sleep(1)
start_app(OFFLINE_APP_NAME)
appThemeScreenshot(offlineDir)
appSearchScreenshot(offlineDir)
appNoticeScreenshot(offlineDir)
appMineScreenshot(offlineDir)

# 截完图后进行diff
sleep(3)
#from ./on_off_diff import *
endPicDiff()
os.system('open ' + three_in_oneDir) # 打开最终生成diff图片的路径
