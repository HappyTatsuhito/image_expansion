#!/usr/bin/env python
# -*- coding: utf-8 -*

import cv2
import numpy as np
import os
import random
import termios
import sys

class ImageExpansion:
    def __init__(self):
        self.PKG_DIR = os.getcwd()[:-8]
        self.BGI_PATH = '/background_image/' #背景画像のパス
        self.LF_NAME = '100' #データ拡張した画像とラベル座標テキストが保存されるフォルダ名
        self.OBJ_GAMMA = 1.0 #オブジェクトの明るさの変更
        self.COLOR_LOWER = np.array([89,90,23], np.uint8)
        self.COLOR_UPPER = np.array([110,255,255], np.uint8)
        self.mouse_event = -1
        self.l_clk = -1
        self.l_dbclk = -1
        self.mouse_x = 0
        self.mouse_y = 0

    def viewImage(self, hsv_img):
        img = hsv_img
        cv2.namedWindow("Show Image")
        cv2.imshow("Show Image", img)
        input_key = cv2.waitKey(0)
        return input_key

    def extractObjectArea(self, img):
        kernel_c = np.ones((10,10),np.uint8)
        look_up_table = np.ones((256, 1), dtype = 'uint8' ) * 0
        black_img = np.zeros((480, 640, 3), np.uint8)
        expanded_black_img = cv2.cvtColor(black_img, cv2.COLOR_BGR2GRAY)
        shrinked_black_img = expanded_black_img.copy()
        wb_img = cv2.imread(self.PKG_DIR + '/other_file/white_back.jpg', 1)
        wb_img = cv2.resize(wb_img, (640, 480))
        wb_img = cv2.cvtColor(wb_img, cv2.COLOR_BGR2HSV)
        input_key = 0
        while input_key != ord('s'):
            if self.COLOR_LOWER[0] > self.COLOR_UPPER[0]:
                print 'in'
                COLOR_INTERMEDIATE = np.array([180, self.COLOR_UPPER[1], self.COLOR_UPPER[2]], np.uint8)
                img_mask_1 = cv2.inRange(img, self.COLOR_LOWER, COLOR_INTERMEDIATE)
                COLOR_INTERMEDIATE = np.array([0,self.COLOR_LOWER[1], self.COLOR_LOWER[2]] , np.uint8)
                img_mask_2 = cv2.inRange(img, COLOR_INTERMEDIATE, self.COLOR_UPPER)
                img_mask = cv2.bitwise_or(img_mask_1, img_mask_2)
            else:
                img_mask= cv2.inRange(img,self.COLOR_LOWER,self.COLOR_UPPER)
            expanded_img_mask = cv2.bitwise_or(img_mask, expanded_black_img)
            shrinked_img_mask = cv2.bitwise_or(cv2.bitwise_not(expanded_img_mask), shrinked_black_img)
            img_mask = cv2.bitwise_not(shrinked_img_mask)
            opening_img = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel_c)
            reverced_img = cv2.bitwise_not(opening_img)
            obj_img = cv2.bitwise_and(img, img, mask = reverced_img)
            obj_img = cv2.cvtColor(obj_img, cv2.COLOR_HSV2BGR)
            for i in range(256):
                look_up_table[i][0] = 255 * pow(float(i) / 255, 1.0 / self.OBJ_GAMMA)
            obj_img = cv2.LUT(obj_img, look_up_table)
            print 'self.COLOR_LOWER : ', self.COLOR_LOWER
            print 'self.COLOR_UPPER : ', self.COLOR_UPPER
            print 'Brightness : ', self.OBJ_GAMMA
            print '\n-------------------------------\n'
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
            print '   - s - : determine the image\n'
            print '-------------------------------\n'
            obj_area_wb_img = cv2.bitwise_and(wb_img, wb_img, mask = opening_img)
            obj_area_wb_img = cv2.cvtColor(obj_area_wb_img, cv2.COLOR_HSV2BGR)
            obj_wb_img = cv2.bitwise_or(obj_img, obj_area_wb_img)
            h, w = obj_wb_img.shape[0], obj_wb_img.shape[1]
            cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
            cv2.setMouseCallback('Image', self.editImage)
            cv2.line(obj_wb_img, (self.mouse_x, 0), (self.mouse_x, h - 1), (255, 0, 0 ))
            cv2.line(obj_wb_img, (0, self.mouse_y), (w - 1, self.mouse_y), (255, 0, 0))
            if self.l_dbclk == 1:
                expanded_black_img = cv2.circle(expanded_black_img, (self.mouse_x, self.mouse_y), 1, (0, 0, 0), -1)
                shrinked_black_img = cv2.circle(shrinked_black_img, (self.mouse_x, self.mouse_y), 1, (255, 255, 255), -1)
            elif self.l_clk == 1:
                expanded_black_img = cv2.circle(expanded_black_img, (self.mouse_x, self.mouse_y), 1, (255, 255, 255), -1)
                shrinked_black_img = cv2.circle(shrinked_black_img, (self.mouse_x, self.mouse_y), 1, (0, 0, 0), -1)
            cv2.imshow('Image', obj_wb_img)
            input_key = cv2.waitKey(1)
            if input_key == ord('r'):
                self.OBJ_GAMMA += 0.05
            elif input_key == ord('f'):
                if self.OBJ_GAMMA > 0.05:
                    self.OBJ_GAMMA -= 0.05
            elif input_key == ord('t'):
                self.COLOR_LOWER[0] += 1
                self.COLOR_LOWER[0] %= 181
            elif input_key == ord('g'):
                self.COLOR_LOWER[0] -= 1
                if self.COLOR_LOWER[0] == 255:
                    self.COLOR_LOWER[0] = 180
                    self.COLOR_LOWER[0] %= 181
            elif input_key == ord('y'):
                self.COLOR_UPPER[0] += 1
                self.COLOR_UPPER[0] %= 181
            elif input_key == ord('h'):
                self.COLOR_UPPER[0] -= 1
                if self.COLOR_UPPER[0] == 255:
                    self.COLOR_UPPER[0] = 180
                    self.COLOR_UPPER[0] %= 181
            elif input_key == ord('u'):
                self.COLOR_LOWER[1] += 1
            elif input_key == ord('j'):
                self.COLOR_LOWER[1] -= 1
            elif input_key == ord('i'):
                self.COLOR_UPPER[1] += 1
            elif input_key == ord('k'):
                self.COLOR_UPPER[1] -= 1
            elif input_key == ord('o'):
                self.COLOR_LOWER[2] += 1
            elif input_key == ord('l'):
                self.COLOR_LOWER[2] -= 1
            elif input_key == ord('p'):
                self.COLOR_UPPER[2] += 1
            elif input_key == ord(';'):
                self.COLOR_UPPER[2] -= 1
            elif input_key == ord('s'):
                obj_img, opening_img, reverced_img, label_obj_img, text = self.createLabel(img, reverced_img, obj_img)
                bb_img = cv2.imread(self.PKG_DIR + '/other_file/blue.jpg', 1)
                bb_img = cv2.cvtColor(bb_img, cv2.COLOR_BGR2HSV)
                bb_img = cv2.bitwise_and(bb_img, bb_img, mask = opening_img)
                bb_img = cv2.cvtColor(bb_img, cv2.COLOR_HSV2BGR)
                obj_bb_img = cv2.bitwise_or(label_obj_img, bb_img)
                print 'Keyboard menu :'
                print '   - s - : save this image'
                print '   - d - : delete this image'
                print '   - c - : finish this program'
                print '   - b - : return to setting'
                print '   other : pass'
                print '\n-------------------------------\n'
                second_input_key = self.viewImage(obj_bb_img)
                if second_input_key == ord('b'):
                    input_key = 0
        return obj_img, opening_img, reverced_img, label_obj_img, text, second_input_key

    def createLabel(self, img, reverced_img, obj_img):
        imgEdge,contours,hierarchy = cv2.findContours(reverced_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours_num = len(contours)
        contours_list = []
        for i in range(contours_num):
            contours_list.append(len(contours[i]))
        object_index = contours_list.index(max(contours_list))
        obj_x,obj_y,obj_w,obj_h = cv2.boundingRect(contours[object_index])
        img_height, img_width = obj_img.shape[:2]
        convert_x = float(obj_x+obj_x+obj_w)/2.0/img_width
        convert_y = float(obj_y+obj_y+obj_h)/2.0/img_height
        convert_w = float(obj_w)/img_width
        convert_h = float(obj_h)/img_height
        print 'Coordinate : (',obj_x,',',obj_y,'),(',obj_x+obj_w,',',obj_y+obj_h,')'
        print 'Annotation : ',convert_x,' ',convert_y,' ',convert_w,' ',convert_h, '\n'
        for i in range(len(contours_list)):
            if i == object_index:
                pass
            else:
                x,y,w,h = cv2.boundingRect(contours[i])
                if x < obj_x or obj_x+obj_w < x:
                    reverced_img = cv2.rectangle(reverced_img,(x, y), (x+w, y+h),(0,0,0), -1)
                elif y < obj_y or obj_y+obj_h < y:
                    reverced_img = cv2.rectangle(reverced_img,(x, y), (x+w, y+h),(0,0,0), -1)
                elif x >= obj_x and x <= obj_x+obj_w:
                    reverced_img = cv2.rectangle(reverced_img,(x, y), (x+w, y+h),(255,255,255), -1)
                elif y >= obj_y and y <= obj_y+obj_h:
                    reverced_img = cv2.rectangle(reverced_img,(x, y), (x+w, y+h),(255,255,255), -1)
        text = ' ' + str(convert_x) + ' ' + str(convert_y) + ' ' + str(convert_w) + ' ' + str(convert_h) + '\n'
        kernel_c = np.ones((30,30),np.uint8)
        reverced_img = cv2.morphologyEx(reverced_img, cv2.MORPH_CLOSE, kernel_c)
        opening_img = cv2.bitwise_not(reverced_img)
        obj_img = cv2.bitwise_and(img, img, mask = reverced_img)
        obj_img = cv2.cvtColor(obj_img, cv2.COLOR_HSV2BGR)
        obj_img_copy = obj_img.copy()
        label_obj_img = cv2.rectangle(obj_img_copy,(obj_x,obj_y),(obj_x+obj_w,obj_y+obj_h),(0,255,0),10)
        return obj_img, opening_img, reverced_img, label_obj_img, text

    def editImage(self, event, x, y, flag, params):
        self.mouse_event = event
        self.mouse_x = x
        self.mouse_y = y
        if self.mouse_event == cv2.EVENT_LBUTTONDBLCLK:
            print 'db'
            self.mouse_event = 0
            self.l_dbclk = 1
        elif self.mouse_event == cv2.EVENT_LBUTTONDOWN:
            print 'clk'
            self.mouse_event = 0
            self.l_clk = 1
        if self.mouse_event == cv2.EVENT_LBUTTONUP:
            print 'up'
            self.l_clk = -1
            self.l_dbclk = -1
    
    def main(self):
        os.system('rm ' + self.PKG_DIR + '/text/test.txt')
        os.system('rm ' + self.PKG_DIR + '/text/train.txt')
        train_file = open(self.PKG_DIR + '/text/test.txt', 'w')
        train_file.close()
        test_file = open(self.PKG_DIR + '/text/train.txt', 'w')
        test_file.close()
        learning_file_exist = os.path.exists(self.PKG_DIR + '/learning')
        if not learning_file_exist:
            print 'Created learning file!'
            os.mkdir(self.PKG_DIR + '/learning')
        LF_exist = os.path.exists(self.PKG_DIR + '/learning/' + self.LF_NAME)
        if not LF_exist:
            print 'Created new file!'
            os.mkdir(self.PKG_DIR + '/learning/' + self.LF_NAME)
        obj_num = 0
        for file_num in os.listdir(self.PKG_DIR + '/image'):
            if file_num[0] == '.':
                continue
            print '\n', file_num, '\n'
            obj_count = 0
            for img_file in os.listdir(self.PKG_DIR + '/image/' + file_num):
                print obj_count
                img_bgr = cv2.imread(self.PKG_DIR + "/image/" + file_num + '/' + img_file, 1)
                img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
                obj_img, obj_area_img, reverced_img,label_obj_img , label_text, input_key = self.extractObjectArea(img)
                if input_key == ord('s'):
                    print 'Loading...'
                    bg_all_list = []
                    for file in os.listdir(self.PKG_DIR + self.BGI_PATH):
                        bg_all_list.append(file)
                    bg_list = []
                    for i in range(400):
                        bg_name = random.choice(bg_all_list)
                        bg_list.append(bg_name)
                        bg_all_list.remove(bg_name)
                    bg_count = 0 
                    for bg_file in bg_list:
                        obj_gamma = random.uniform(1.0, 2.0)
                        bg_img = cv2.imread(self.PKG_DIR + self.BGI_PATH + bg_file, 1)
                        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2HSV)
                        bg_img = cv2.bitwise_and(bg_img, bg_img, mask = obj_area_img)
                        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_HSV2BGR)
                        gen_img= cv2.bitwise_or(obj_img, bg_img)
                        look_up_table = np.ones((256, 1), dtype = 'uint8' ) * 0
                        gen_gamma = random.uniform(0.3, 2.5)
                        for i in range(256):
                            look_up_table[i][0] = 255 * pow(float(i) / 255, 1.0 / gen_gamma)
                        gen_img = cv2.LUT(gen_img, look_up_table)
                        cv2.imwrite(self.PKG_DIR + '/learning/' + self.LF_NAME + '/' + str(int(file_num)) + '_' + str(obj_count) + '_' + str(bg_count) + '.jpg',gen_img)
                        label_txt = open(self.PKG_DIR + '/learning/' + self.LF_NAME + '/' + str(int(file_num))+ '_' + str(obj_count) + '_' + str(bg_count) + '.txt', 'w')
                        txt = str(int(file_num)) + label_text
                        label_txt.write(txt)
                        label_txt.close()
                        learning_txt = '/home/demulab/src/darknet3/athome_cfg/' + self.LF_NAME + '/' + str(int(file_num)) + '_' + str(obj_count) + '_' + str(bg_count) + '.jpg\n'
                        if bg_count < 320:
                            t_txt = self.PKG_DIR + '/text/train.txt'
                        else :
                            t_txt = self.PKG_DIR + '/text/test.txt'
                        learning_txt_file = open(t_txt, 'a')
                        learning_txt_file.write(learning_txt)
                        learning_txt_file.close()
                        bg_count += 1
                    print 'Saved!'
                elif input_key == ord('d'):
                    print img_file
                    os.system('rm ' + self.PKG_DIR + '/image/' + file_num + '/' + img_file)
                elif input_key == ord('c'):
                    break
                print '\n\n\n\n\n\n\n\n'
                obj_count += 1
        obj_num += 1


if __name__ == '__main__':
#    rospy.init_node('tm_image_expansion')
    image_expansion = ImageExpansion()
    image_expansion.main()
