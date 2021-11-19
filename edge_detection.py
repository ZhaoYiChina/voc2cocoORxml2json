#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : George Zhao
@Contact :  : zhaoyipassion@gmail.com
@Software: PyCharm
@File    : edge_detection.py
@Date    : 2021/2/27
@Desc    :  null
"""

"""
cv2.Canny(image,            # 输入原图（必须为单通道图）
          threshold1, 
          threshold2,       # 较大的阈值2用于检测图像中明显的边缘
          [, edges[, 
          apertureSize[,    # apertureSize：Sobel算子的大小
          L2gradient ]]])   # 参数(布尔值)：
                              true： 使用更精确的L2范数进行计算（即两个方向的倒数的平方和再开放），
                              false：使用L1范数（直接将两个方向导数的绝对值相加）。
"""

import cv2
import numpy as np

path = '../test/marked'  # 待检测图片的位置
image_path = path + '/' + '000005.jpg'
image_label_path = path + '/' + '000005_label.jpg'
canny_path = path + '/' + 'object_000005.jpg'

object_path = path + '/' + '1.png'

object_path_2 = path + '/' + '2.png'

object_path_contours = path + '/' + 'object_path_contours.png'

object_path_new = path + '/' + 'object_path_new.png'

object_path_kai = path + '/' + 'object_path_kai.png'

object_path_bi = path + '/' + 'object_path_bi.png'

object_path_outline1 = path + '/' + 'object_path_outline1.png'

object_path_outline2 = path + '/' + 'object_path_outline2.png'

def detection():

    original_img = cv2.imread(image_path, 0)

    # canny(): 边缘检测
    img1 = cv2.GaussianBlur(original_img, (3, 3), 0)
    canny = cv2.Canny(img1, 50, 150)

    # 形态学：边缘检测
    _, Thr_img = cv2.threshold(original_img, 210, 255, cv2.THRESH_BINARY)  # 设定红色通道阈值210（阈值影响梯度运算效果）
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 定义矩形结构元素
    gradient = cv2.morphologyEx(Thr_img, cv2.MORPH_GRADIENT, kernel)  # 梯度

    cv2.imshow("original_img", original_img)
    cv2.imshow("gradient", gradient)
    cv2.imshow('Canny', canny)

    cv2.imwrite(canny_path, canny)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def preProcess():

    img = cv2.imread(object_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow("gray", gray)

    ret, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    cv2.imshow("binary", binary)

    kernel = np.ones((6, 6), dtype=np.uint8)
    # opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, 1)
    # ss = np.hstack((binary, opening))

    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)  ## 有缺陷，填补缺陷

    cv2.imshow('closing', closing)

    cv2.imwrite(object_path_bi, closing)

    cv2.waitKey(0)

def outline1():


    img = cv2.imread(object_path)
    closing = cv2.imread(object_path,  cv2.CV_8UC1)
    cv2.imshow("closing", closing)

    contours, hierarchy = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0,255,0),3)

    # 计算轮廓面积
    area = 0
    for i in contours:
        area += cv2.contourArea(i)
    print(area)

    cv2.imshow("outline1", closing)

    cv2.imwrite(object_path_outline1, closing)

    cv2.waitKey(0)

def outline2():

    # 读取文件
    mat_img = cv2.imread(image_path)
    #mat_img2 = cv2.imread(image_path, cv2.CV_8UC1)

    # #top: 151、 bottom: 206、 left: 233、 right: 330
    cv2.imshow('object', mat_img[151:206, 233:330])
    mat_img2 = mat_img[151:206, 233:330]
    cv2.imwrite(object_path_2, mat_img2)

    img = cv2.imread(object_path_2)

    mat_img = cv2.imread(object_path_bi)
    mat_img2 = cv2.imread(object_path_bi, cv2.CV_8UC1)

    # 自适应分割
    dst = cv2.adaptiveThreshold(mat_img2, 210, cv2.BORDER_REPLICATE, cv2.THRESH_BINARY_INV, 3, 10)
    cv2.imshow("window1", dst)
    cv2.imwrite(object_path_outline2, dst)
    # 提取轮廓
    contours, heridency = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)

    # 标记轮廓
    #cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

    array = contours[0]


    print(contours[0])

    minx0 = 0
    for i in contours[0]:
        #print(i[0][0])
        for j in contours[0]:
            minx = abs(j[0][1]-(i)[0][1])
            if(minx > minx0):
                minx0 = minx
                print(minx0)

    print(minx0)

    print(".....................")
    miny0 = 0
    for i in contours[0]:
        #print(i[0][0])
        for j in contours[0]:
            miny = abs(j[0][0]-(i)[0][0])
            if(miny > miny0):
                miny0 = miny
                print(miny0)

    print(miny0)




    # 计算轮廓面积
    area = 0
    for i in contours:
        area += cv2.contourArea(i)
    print(area)

    # 图像show
    cv2.imshow("window2", img)
    cv2.imwrite(object_path_contours, img)

    cv2.waitKey(0)

def outline3():


    #读取文件
    origin_imgae = cv2.imread(image_path)

    object_contours = cv2.imread(object_path_contours)

    #top: 151、 bottom: 206、 left: 233、 right: 330
    #cv2.imshow('object', mat_img[151:206, 233:330])
    #mat_img2 = mat_img[151:206, 233:330]

    origin_imgae[151:206, 233:330] = object_contours

    cv2.imshow('image_label', origin_imgae)

    cv2.imwrite(image_label_path, origin_imgae)


def process():

    # 读取文件
    mat_img = cv2.imread(image_path)

    # #top: 151、 bottom: 206、 left: 233、 right: 330
    mat_img2 = mat_img[151:206, 233:330]

    gray = cv2.cvtColor(mat_img2, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    kernel = np.ones((6, 6), dtype=np.uint8)
    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)  ## 有缺陷，填补缺陷
    cv2.imwrite(object_path_bi, closing)
    mat_img2 = cv2.imread(object_path_bi, cv2.CV_8UC1)

    # 自适应分割
    dst = cv2.adaptiveThreshold(mat_img2, 210, cv2.BORDER_REPLICATE, cv2.THRESH_BINARY_INV, 3, 10)
    # 提取轮廓
    contours, heridency = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)

    cv2.imshow("contours", contours[0])

    cv2.waitKey(0)

    minx0 = 0
    for i in contours[0]:
        for j in contours[0]:
            minx = abs(j[0][1] - (i)[0][1])
            if (minx > minx0):
                minx0 = minx

    miny0 = 0
    for i in contours[0]:
        for j in contours[0]:
            miny = abs(j[0][0] - (i)[0][0])
            if (miny > miny0):
                miny0 = miny

    print(minx0/10)
    print(".....................")
    print(miny0/10)

    # 计算轮廓面积
    area = 0
    for i in contours:
        area += cv2.contourArea(i)
    print(area/100)

if __name__ == '__main__':
    #preProcess()
    outline2()
   # process()
    # outline3()
    # detection()
    print('edge_detection' + 'was called')
