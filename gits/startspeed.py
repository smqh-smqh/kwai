# -*- encoding=utf8 -*-
__author__ = "wyx"
import time
import threading
import os
import shutil
import sys
import signal
import subprocess
import cv2 as cv
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.core.cv import Template, loop_find3, try_log_screen
from poco.drivers.ios import iosPoco


# script content
# start_app('tv.acfun.video')
# timestart = time.time()
print("start...")
DEVICEID2 = '00008020-000C395A0260802E'
# DEVICEID2 = '00008020-0001489436C3002E'
os_command_record_bili = '/Users/wyx/Documents/xrecord/bin/xrecord --quicktime --i={} --out=./test_bili.mp4 --force'.format(DEVICEID2)
os_command_record_online = '/Users/wyx/Documents/xrecord/bin/xrecord --quicktime --i={} --out=./test_acfun.mp4 --force'.format(DEVICEID2)
os_command_list = '/Users/wyx/Documents/xrecord/bin/xrecord --list'
os_command_grep = "ps -ef |grep " + DEVICEID2 + "|grep debug|awk '{print $2}'"
os_command_kill = "ps -ef |grep " + DEVICEID2 + "|grep -v 'grep' |awk '{print $2}' |xargs kill -9"


class StoppableThread(threading.Thread):

    def __init__(self ,command, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.command = command

    def stop(self):
        self._stop_event.set()

    def start(self):
        print(self.command)
        # os.popen(os_command_record)
        os.popen(self.command)

        
        
def split_frame(video_name,pic_path):
    print('spliting....')
    if os.path.exists(pic_path):
        shutil.rmtree(pic_path)
    os.mkdir(pic_path)
    vidcap = cv.VideoCapture(video_name)
    success,image = vidcap.read()

    count = 0
    success = True
    while success:
        success,image = vidcap.read()
        # print(type(image))
        # print("大小：",image.shape)
        milliseconds = vidcap.get(cv.CAP_PROP_POS_MSEC)
        cv.imwrite(pic_path +"frame%04d_%d.jpg" % (count,milliseconds), image)     # save frame as JPEG file
        # if cv.waitKey(10) == 27:                     
        #     break
        count += 1
        

def find_tag(file_path):
    print('finding tag...')
    file_path_online = file_path
#     file_path_offline = file_path
    files_online = os.listdir(file_path_online)
#     files_online.sort()
    files_online.sort(key= lambda x:int(x.split('_')[0][5:]))
    print(files_online)
    for i in range(len(files_online)-2):
#         print(files_online[i])
        if "jpg" not in  files_online[i]:
            continue
        print(file_path_online+ files_online[i])
        loop_find3_result = loop_find3(file_path_online+ files_online[i],Template(r"tpl1605064959952.png", record_pos=(0.239, -0.426), resolution=(828, 1792)),posi=(426, 577), tag="精选", timeout=1,threshold=0.99)
#         loop_find3_result = loop_find3('./picSplitOnline/frame246_4668.jpg',Template(r"tpl1605064959952.png", record_pos=(0.239, -0.426), resolution=(828, 1792)),posi=(426, 577),tag="精选",timeout=1, threshold=0.90)

        # if loop_find3_result:
        #     print(pics)
        if loop_find3_result:
            print("success")
            return files_online[i]
#             print("loop_find3_result%d"%i, loop_find3_result)


def test_app(app_name,path,video_name):
    ONLINE_APP_NAME  = app_name
    stop_app(ONLINE_APP_NAME)
    sleep(3)
    os_command_record = '/Users/wyx/Documents/xrecord/bin/xrecord --quicktime --i={} --out={} --force'.format(DEVICEID2,video_name)
    t = StoppableThread(os_command_record)
    t.start()
    imestart = time.time()
    start_app(ONLINE_APP_NAME)
    sleep(4)
    t.stop()
    pids = os.popen(os_command_grep).read()
    for pid in pids.split("\n"):
        if pid == "":
            continue
        print("pid",pid)
        os.kill(int(pid),2)
    os.popen(os_command_kill)       
    stop_app(ONLINE_APP_NAME)
    split_frame(video_name,path)



def test_acfun():
    test_app('tv.acfun.video')
    path='./picSplitOnline/'
        #分帧
    split_frame('test_acfun.mp4',path)
        #识别
    name=find_tag(path)
    time=name.split('_')[1][:-4]
    print("acfun: "+time)
        
    
def test_blibli():
    test_app('tv.danmaku.bilianime')
    path='./picSplitBlibli/'
#        分帧
    split_frame('test_bili.mp4',path)
#         识别
    name=find_tag(path)
    time=name.split('_')[1][:-4]
    print("blibli: "+time)

# loop_find3_result=loop_find3('./picSplitOnline/frame100_1721.jpg',Template(r"tpl1605064959952.png", record_pos=(0.239, -0.426), resolution=(828, 1792)),posi=(30, 577),tag="精选",timeout=1, threshold=0.99)

# if loop_find3_result:
#     print(loop_find3_result)
# find_tag('./picSplitOnline/')


if __name__ == "__main__":
    if not cli_setup():
        auto_setup(__file__, logdir=True, devices=[
                "ios:///http://127.0.0.1:8100",
        ])
    list_result = os.popen(os_command_list)
    devices = list_result.read()
    print(devices)
    if DEVICEID2 not in devices:
        sys.exit("未检测到有效设备")
    else:
        poco = iosPoco()
#     split_frame('android_test_1.mp4','./android_test_1/')    
#     split_frame('ios38.0_1.mp4','./ios38.0_1/')
#     split_frame('ios38.0_2.mp4','./ios38.0_2/')
#     split_frame('ios38.0_3.mp4','./ios38.0_3/')
#     split_frame('ios38.0_4.mp4','./ios38.0_4/')
#     split_frame('ios38.0_5.mp4','./ios38.0_5/')
#     split_frame('android_acfun_3.mp4','./android_acfun_3/')    
#     split_frame('android_acfun_4.mp4','./android_acfun_4/')  
#     split_frame('android_acfun_5.mp4','./android_acfun_5/')
        test_app('tv.acfun.video','./pic2/picSplitAcfun/','test_acfun.mp4')
        test_app('tv.danmaku.bilianime','./pic2/picSplitBili/','test_bili.mp4')
        test_app('com.qiyi.iphone','./pic2/picSplitQiyi/','test_iqiyi4.mp4')
        test_app('com.tencent.live4iphone','./pic2/picSplitTencent/','test_tencent.mp4')
        test_app('com.ss.iphone.ugc.Aweme','./pic2/picSplitByte/','test_byte.mp4')
        test_app('com.jiangjia.gif','./pic2/picSplitkwai/','test_kwai.mp4')
        
