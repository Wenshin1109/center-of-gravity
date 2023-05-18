# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from xml.dom import minidom

def main():
    img_num = "000"
    #SVGtoPNG
    drawing = svg2rlg('./input/'+img_num+'.svg')
    try:    #check if the dir exists
        os.makedirs("./png")
    except FileExistsError:
        renderPM.drawToFile(drawing, './png/'+img_num+'.png', fmt='PNG')
    except PermissionError:
        print("permission denied")
    

    #read the image
    img = cv2.imread('./png/'+img_num+'.png')
    #get image size
    height, width, channels = img.shape
    #pring size
    # print(str(height) + " " + str(width))
    # create empty mat
    binary_img = np.zeros((height, width), np.uint8)
    # rgb to binary
    for i in range(0, height):
        for j in range(0, width):
            r_value = img[i, j, 2]
            g_value = img[i, j, 1]
            b_value = img[i, j, 0]
            binary_img[i, j] = 0.333 * r_value + 0.333 * g_value + 0.333 * b_value
            if binary_img[i, j] < 127:
                binary_img[i, j] = 0
            else:
                binary_img[i, j] = 255

    # cv2.imshow('binary', binary_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # calulate the number of pixels per height
    h_avg = 0
    array_w = np.zeros((height,), np.uint8)
    for i in range(0, height):
        for j in range(0, width):
            if binary_img[i, j] == 0:
                array_w[i] += 1
    # find the index of height which head approximately equal to tail
    for i in range(1, height-2):
        head = sum(array_w[0:i])
        tail = sum(array_w[i:height-1])
        if head >= tail:
            h_avg = i
            break

    # print(h_avg)


    cv2.circle(img, (int(width/2), h_avg), 5, (0, 0, 255), -1)
    cv2.imshow('try', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # edit svg
    cx = int(width/2)
    cy = h_avg
    print(str(cx) + " " + str(cy))
    doc = minidom.parse('./input/'+img_num+'.svg')
    root = doc.documentElement
    circle = doc.createElement('circle')
    circle.setAttribute('cx', str(cx))
    circle.setAttribute('cy', str(cy))
    circle.setAttribute('r', '5')
    circle.setAttribute('fill', 'red')

    root.appendChild(circle)

    try:    #check if the dir exists
        os.makedirs("./output")
    except FileExistsError:
        with open('./output/'+img_num+'.svg', 'w') as f:
            f.write(doc.toxml())
    except PermissionError:
        print("permission denied")

    
    exit(0)


if __name__ == '__main__':
    main()