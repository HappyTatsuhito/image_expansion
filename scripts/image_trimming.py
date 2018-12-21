#!/usr/bin/env python
# -*- coding: utf-8 -*

import cv2
import numpy as np
import os

PKG_DIR = os.getcwd()[:-8]

COLOR_LOWER = np.array([120,90,23], np.uint8)
COLOR_UPPER = np.array([180,255,255], np.uint8)
BACKGROUND_SELECTION = 0
OBJ_GAMMA = 1.0
BG_COUNT = 0


def viewImage(img):
    cv2.namedWindow("Show Image")
    cv2.imshow("Show Image", img)
    input_key = cv2.waitKey(0)
    return input_key

def correctMask(receive_image, gray_scale):
    correct_image = np.ones((480, 640),np.uint8) * gray_scale
    for i in range(479):
        correct_image[i][0:639] = receive_image[i+1][1:640]
    return correct_image

def extractObjectArea(img):
    kernel_c = np.ones((10,10),np.uint8)
    look_up_table = np.ones((256, 1), dtype = 'uint8' ) * 0
    input_key = 0
    while input_key != ord('s'):
        wb_img = cv2.imread(PKG_DIR + '/other_file/white_back.jpg', 1)
        wb_img = cv2.resize(wb_img, (640, 480))
        wb_img = cv2.cvtColor(wb_img, cv2.COLOR_BGR2HSV)
        if COLOR_LOWER[0] > COLOR_UPPER[0]:
            COLOR_INTERMEDIATE = np.array([180, COLOR_UPPER[1], COLOR_UPPER[2]], np.uint8)
            img_mask_1 = cv2.inRange(img, COLOR_LOWER, COLOR_INTERMEDIATE)
            COLOR_INTERMEDIATE = np.array([0,COLOR_LOWER[1], COLOR_LOWER[2]] , np.uint8)
            img_mask_2 = cv2.inRange(img, COLOR_INTERMEDIATE, COLOR_UPPER)
            img_mask = cv2.bitwise_or(img_mask_1, img_mask_2)
        else:
            img_mask= cv2.inRange(img,COLOR_LOWER,COLOR_UPPER)
        opening_img = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel_c)
        opening_img = correctMask(opening_img, 0)
        reverced_img = cv2.bitwise_not(opening_img)
        obj_img = cv2.bitwise_and(img, img, mask = reverced_img)
        obj_img = cv2.cvtColor(obj_img, cv2.COLOR_HSV2BGR)
        global OBJ_GAMMA
        for i in range(256):
            look_up_table[i][0] = 255 * pow(float(i) / 255, 1.0 / OBJ_GAMMA)
        obj_img = cv2.LUT(obj_img, look_up_table)
        print '\nCOLOR_LOWER : ', COLOR_LOWER
        print 'COLOR_UPPER : ', COLOR_UPPER
        print 'Brightness : ', OBJ_GAMMA
        print '\n-------------------------------'
        print 'Keyboard menu :'
        print '   - r - : increase brightness'
        print '   - f - : decrease brightness'
        print '   - t - : increase lower[0]'
        print '   - g - : decrease lower[0]'
        print '   - y - : increase upper[0]'
        print '   - h - : decrease upper[0]'
        print '   - u - : increase lower[1]'
        print '   - j - : decrease lower[1]'
        print '   - i - : increase upper[1]'
        print '   - k - : decrease upper[1]'
        print '   - o - : increase lower[2]'
        print '   - l - : decrease lower[2]'
        print '   - p - : increase upper[2]'
        print '   - ; - : decrease upper[2]'
        print '   - s - : determine the image'
        print '-------------------------------'
        wb_img = cv2.bitwise_and(wb_img, wb_img, mask = opening_img)
        wb_img = cv2.cvtColor(wb_img, cv2.COLOR_HSV2BGR)
        obj_wb_img = cv2.bitwise_or(obj_img, wb_img)
        input_key = viewImage(obj_wb_img)
        if input_key == ord('r'):
            OBJ_GAMMA += 0.05
        elif input_key == ord('f'):
            if OBJ_GAMMA > 0.05:
                OBJ_GAMMA -= 0.05
            else :
                pass
        elif input_key == ord('t'):
            COLOR_LOWER[0] += 1
            COLOR_LOWER[0] %= 181
        elif input_key == ord('g'):
            COLOR_LOWER[0] -= 1
            if COLOR_LOWER[0] == 255:
                COLOR_LOWER[0] = 180
            COLOR_LOWER[0] %= 181
        elif input_key == ord('y'):
            COLOR_UPPER[0] += 1
            COLOR_UPPER[0] %= 181
        elif input_key == ord('h'):
            COLOR_UPPER[0] -= 1
            if COLOR_UPPER[0] == 255:
                COLOR_UPPER[0] = 180
            COLOR_UPPER[0] %= 181
        elif input_key == ord('u'):
            COLOR_LOWER[1] += 1
        elif input_key == ord('j'):
            COLOR_LOWER[1] -= 1
        elif input_key == ord('i'):
            COLOR_UPPER[1] += 1
        elif input_key == ord('k'):
            COLOR_UPPER[1] -= 1
        elif input_key == ord('o'):
            COLOR_LOWER[2] += 1
        elif input_key == ord('l'):
            COLOR_LOWER[2] -= 1
        elif input_key == ord('p'):
            COLOR_UPPER[2] += 1
        elif input_key == ord(';'):
            COLOR_UPPER[2] -= 1
        elif input_key == ord('s'):
            loop_flg = 1
            global BG_COUNT
            while loop_flg:
                loop_flg = 0
                obj_img, opening_img, reverced_img, labeled_obj_img = createLabel(reverced_img, obj_img)
                obj_img = cv2.LUT(obj_img, look_up_table)
                if BG_COUNT == 0:
                    bg_path = 'blue_back.jpg'
                elif BG_COUNT == 1:
                    bg_path = 'green_back.jpg'
                elif BG_COUNT == 2:
                    bg_path = 'red_back.jpg'
                bg_img = cv2.imread(PKG_DIR + '/other_file/' + bg_path, 1)
                bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2HSV)
                bg_img = cv2.bitwise_and(bg_img, bg_img, mask = opening_img)
                bg_img = cv2.cvtColor(bg_img, cv2.COLOR_HSV2BGR)
                labeled_monochromatic_img = cv2.bitwise_or(labeled_obj_img, bg_img)
                monochromatic_img = cv2.bitwise_or(obj_img, bg_img)
                print '-------------------------------'
                print 'Keyboard menu :'
                print '   - s - : save this image'
                print '   - d - : delete this image'
                print '   - c - : finish this program'
                print '   - b - : return to set'
                print '   other : pass'
                print '-------------------------------'
                second_input_key = viewImage(labeled_monochromatic_img)
                if second_input_key == ord('b'):
                    input_key = 0
                elif second_input_key == 81:
                    loop_flg = 1
                    BG_COUNT -= 1
                    BG_COUNT %= 3
                elif second_input_key == 83:
                    loop_flg = 1
                    BG_COUNT += 1
                    BG_COUNT %= 3
    return monochromatic_img, second_input_key

def createLabel(reverced_img, obj_img):
    imgEdge,contours,hierarchy = cv2.findContours(reverced_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours_num = len(contours)
    contours_list = []
    for i in range(contours_num):
        contours_list.append(len(contours[i]))
    object_index = contours_list.index(max(contours_list))
    obj_x,obj_y,obj_w,obj_h = cv2.boundingRect(contours[object_index])
    img_height, img_width = img_bgr.shape[:2]
    convert_x = float(obj_x+obj_x+obj_w)/2.0/img_width
    convert_y = float(obj_y+obj_y+obj_h)/2.0/img_height
    convert_w = float(obj_w)/img_width
    convert_h = float(obj_h)/img_height
    for i in range(len(contours_list)):
        if i == object_index:
            continue
        else:
            x,y,w,h = cv2.boundingRect(contours[i])
            if (x >= obj_x and x <= obj_x+obj_w) and (y >= obj_y and y <= obj_y+obj_h):
                reverced_img = cv2.rectangle(reverced_img,(x, y), (x+w, y+h),(255,255,255), -1)
    black_img = np.zeros((480, 640, 3), np.uint8)
    black_img = cv2.cvtColor(black_img, cv2.COLOR_BGR2GRAY)
    black_img = cv2.rectangle(black_img, (obj_x,obj_y), (obj_x+obj_w,obj_y+obj_h),(255,255,255),-1)
    reverced_img = cv2.bitwise_and(reverced_img, black_img)
    kernel_c = np.ones((30,30),np.uint8)
    reverced_img = cv2.morphologyEx(reverced_img, cv2.MORPH_CLOSE, kernel_c)
    reverced_img = correctMask(reverced_img, 255)
    obj_img = cv2.bitwise_and(img, img, mask = reverced_img)
    obj_img = cv2.cvtColor(obj_img, cv2.COLOR_HSV2BGR)
    opening_img = cv2.bitwise_not(reverced_img)
    obj_img_copy = obj_img.copy()
    label_obj_img = cv2.rectangle(obj_img_copy,(obj_x,obj_y),(obj_x+obj_w,obj_y+obj_h),(255,255,255),10)
    return obj_img, opening_img, reverced_img, label_obj_img

def checkFileExist():
    obj_count = 0
    trimed_image_exist = os.path.exists(PKG_DIR + '/trimed_image')
    if trimed_image_exist:
        trimed_image_file_exist = os.path.exists(PKG_DIR + '/trimed_image/' + file_num)
        if trimed_image_file_exist:
            trimed_image_file_list = os.listdir(PKG_DIR + '/trimed_image/' + file_num)
            if len(trimed_image_file_list) > 0:
                obj_count = int((sorted(trimed_image_file_list)[len(trimed_image_file_list) - 1])[2]) + 1
        else:
            print 'Created new trimed_image file ' + str(file_num) + '!'
            os.mkdir(PKG_DIR + '/trimed_image/' + file_num)
    else:
        print 'Created trimed_image file!'
        os.mkdir(PKG_DIR + '/trimed_image')
        os.mkdir(PKG_DIR + '/trimed_image/' + file_num)
        
    expanded_image_exist = os.path.exists(PKG_DIR + '/expanded_image')
    if expanded_image_exist:
        expanded_image_file_exist = os.path.exists(PKG_DIR + '/expanded_image/' + file_num)
        if not expanded_image_file_exist:
            print 'Created new expanded_image file ' + str(file_num) + '!'
            os.mkdir(PKG_DIR + '/expanded_image/' + file_num)
    else:
        print 'Created expanded_image file!'
        os.mkdir(PKG_DIR + '/expanded_image')
        os.mkdir(PKG_DIR + '/expanded_image/' + file_num)
    return obj_count

if __name__ == '__main__':
    for file_num in os.listdir(PKG_DIR + '/image'):
        if file_num[0] == '.':
            continue
        print '\n', file_num, '\n'
        obj_count = checkFileExist()
        for img_file in os.listdir(PKG_DIR + '/image/' + file_num):
            img_bgr = cv2.imread(PKG_DIR + "/image/" + file_num + '/' + img_file, 1)
            img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            obj_img, input_key = extractObjectArea(img)
            if input_key == ord('s'):
                print 'Loading...'
                cv2.imwrite(PKG_DIR + '/trimed_image/' + file_num + '/' + str(int(file_num)) + '_' + str(obj_count) + '.jpg',obj_img)
                print 'Saved!'
                os.system('mv ' + PKG_DIR + '/image/' + file_num + '/' + img_file + ' ' + PKG_DIR + '/expanded_image/' + file_num)
                obj_count += 1
            elif input_key == ord('d'):
                print img_file
                os.system('rm ' + PKG_DIR + '/image/' + file_num + '/' + img_file)
            elif input_key == ord('c'):
                break
            print '\n'
