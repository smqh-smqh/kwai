from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import numpy as np
from PIL import Image
import math
import operator
from functools import reduce 
from picture_duibi import calc_similar_by_path
from operator import ge

def calc(img1,img2):
    picSim = calc_similar_by_path(img1,img2)
    print(round(picSim,2))

np.set_printoptions(threshold=np.inf)

def absdiff_demo(image_1, image_2, sThre):
    gray_image_1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)  # 灰度化
    gray_image_1 = cv2.GaussianBlur(gray_image_1, (5, 5), 0)  # 高斯滤波
    gray_image_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)
    gray_image_2 = cv2.GaussianBlur(gray_image_2, (5, 5), 0)
    # cv2.imwrite('img1.jpg',gray_image_1)
    # cv2.imwrite('img2.jpg',gray_image_2)
    # calc('img1.jpg','img2.jpg')
    d_frame = cv2.absdiff(gray_image_1, gray_image_2)
    # d_frame = gray_image_1-gray_image_2
    ret, d_frame = cv2.threshold(d_frame, sThre, 255, cv2.THRESH_BINARY)
    return d_frame


def picdiff():
    img1 = cv2.imread("./frame132.jpg")
    img2 = cv2.imread("./frame113.jpg")
    img_result = absdiff_demo(img1,img2,10)
    # img_result = img1-img2
    # img_result=cv2.cvtColor(img_result, cv2.THRESH_BINARY)
    # cv2.imshow("img_result",img_result)
    similar=1-(len(img_result[img_result==255])/(len(img_result[img_result==255])+len(img_result[img_result==0])))
    print(round(similar,5))
    cv2.waitKey(0)
    

# img1="./frame132.jpg"
# img2="./frame113.jpg"
picdiff()
