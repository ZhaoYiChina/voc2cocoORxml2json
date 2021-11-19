#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : George Zhao
@Contact :  : zhaoyipassion@gmail.com
@Software: PyCharm
@File    : get_accuracy.py
@Date    : 2021/2/27
@Desc    :  null
"""

import re

# 创建创建一个存储检测结果的dir
result_path = '../result'
# 创建一个记录检测结果的文件



def processAccuracy():

    accuracy_path = result_path + '/result_doc/result_accuracy.txt'
    accuracy_doc = open(accuracy_path, 'w')

    result_doc_path = result_path + '/result_doc/result.txt'
    result_doc = open(result_doc_path, 'r')
    result_str = result_doc.readlines()
    result_doc.close()

    right_count = 0

    for i in range(1001):
        t = 0
        s = '0'
        l = 5 - len(str(i))
        while(l):
            s += '0'
            l -= 1
        pre = '../VOCdevkit/VOC2021/Annotations/'
        file_name = pre + s + str(i) + '.xml'

        sample_xml_file = open(file_name, 'r')

        sample_data = sample_xml_file.read()

        sample_xml_file.close()

        sample_result = result_str[i].split()

        right_result = False

        for sample_item in sample_result:
            if sample_data.count(sample_item) > 0:
                right_result = True
                break

        if right_result:
            right_count += 1

    accuracy_doc.write("Accuracy is {:.2%}".format(right_count/1000))
    accuracy_doc.close()






if __name__ == '__main__':
    print('get_accuracy' + 'was called')
    processAccuracy()

