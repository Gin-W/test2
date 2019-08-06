# @ Time  : 2019/6/24
# @ Author: wang

#！/usr/bin/env python
# encoding: utf-8
'''
1、遍历某路径下所有文件和文件夹(这个问题和，“指定一个节点，输出以这个节点作为根节点的这棵树的所有子节点”一样。
递归可以实现。如果是叶子节点（文件）了，就输出这个叶子节点的名称，返回。否则，输出这个节点的名称（文件夹），并以这个结点再次作为根节点，遍历输出它的所有子节点)
2、读取文件内容
3、对文件中内容操作
'''
import os
import os.path
import glob
import cv2 as cv
import numpy as np

# 遍历指定目录
def traverse(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        # 用os.listdir()这个函数，只会返回路径下的所有文件名（而这些文件名不含路径）……所以要写成绝对路径。可以用os.path.join这个函数。
        childDir = os.path.join('%s\%s' %(filepath,allDir))
        if not os.path.isdir(childDir):
            print("下一步")
             #print('文件：%s'%childDir)
#            readFile(childDir)
#                print(childDir.decode('gbk')    #解决中文显示乱码问题
        else:
            print('文件夹：%s'%childDir)
            listJPG = glob.glob(os.path.join(childDir, ('*.jpg')))
            for i in listJPG:
                print(i)
                readImage(i)
            traverse(childDir)

# 对每个文件的操作，读取相机内参矩阵和几何畸变参数
def readFile(filenames):
    f = open(filenames, 'r')
    listfile = f.readlines()
    list1 = listfile[2].split()
    list1 = [float(x) for x in list1]
    #list1 = list(map(float,list1))
    # for i,v in enumerate(list1):
    #     list1[i] = float(v)
    #print(list1)
    list2 = listfile[3].split()
    list2 = [float(x) for x in list2]
    list3 = listfile[4].split()
    list3 = [float(x) for x in list3]
    list4 = listfile[6].split()
    list4 = [float(x) for x in list4]
    list1 = np.array(list1)
    list2 = np.array(list2)
    list3 = np.array(list3)
    list_to_matrix = np.matrix([list1,list2,list3])
    new_list_to_matrix = np.matrix([[1,0,0],[0,1,0],[0,0,1]])
    list4_to_array = np.matrix(list4)
    #list4_to_array = list4_to_array.reshape(4,1)

    print(list_to_matrix)
    print(new_list_to_matrix)
    print(list4_to_array)
    f.close()
    return list_to_matrix,list4_to_array,new_list_to_matrix
# 对图像操作,将图像缩放到640*480
def readImage(imagePath):
    writePath = imagePath
    #print(imagePath)
    image = cv.imread(imagePath)  # 图像路径不能有中文
    # 打印出图片尺寸
    print(image.shape)
    # 将图片高和宽分别赋值给x，y
    x, y = image.shape[0:2]
    # 缩放到原来的二分之一，输出尺寸格式为（宽，高）
    # img_test1 = cv.resize(img, (int(y / 2), int(x / 2)))
    # 最近邻插值法缩放
    # 缩放到原来的四分之一
    dst = cv.resize(image, (640, 480), fx=0, fy=0, interpolation=cv.INTER_LINEAR)
    print(dst.shape)
    # cv.namedWindow('input_image',cv.WINDOW_NORMAL)
    # cv.imshow('input_image',image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    cv.imwrite(writePath,dst)
# 图像去畸变操作
def undistort():
    filepath = r'F:\contest\scene1_jiading_lib_training(1)'
    #filepath = r'G:\contest\IntelligentCity\scene1_jiading_lib_training(1)'
    calibration = r'F:\contest\calibration'
    #calibration = r'G:\contest\IntelligentCity\IntelligentCity\calibration'
    intrin = ['intrin_1.txt', 'intrin_2.txt', 'intrin_3.txt', 'intrin_4.txt', 'intrin_5.txt', 'intrin_6.txt']
    for i in intrin:
        calibrationPath = os.path.join(calibration, i)

    list_to_matrix, list4_to_array, new_list_to_matrix = readFile(os.path.join(calibration, 'intrin_1.txt'))
    # image = cv.imread(r'G:\contest\IntelligentCity\scene1_jiading_lib_training(1)\scene1_jiading_lib_training\PIC_20190522_100025\origin_1.jpg')
    image = cv.imread(r'.\0.jpg')
    cv.imshow('image', image)

    undistorted = cv.fisheye.undistortImage(image, list_to_matrix, list4_to_array, list_to_matrix)
    cv.imshow('undistorted', undistorted)
    cv.waitKey(0)

if __name__ =="__main__":
    #filepath = r'G:\contest\IntelligentCity\train\scene1_jiading_lib_training\scene1_jiading_lib_training'
    filepath = r'F:\contest\train\scene1_jiading_lib_training\scene1_jiading_lib_training1'
    traverse(filepath)
    #undistort()

