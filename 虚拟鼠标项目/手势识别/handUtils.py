"""
作者：zwq
日期:2022年01月23日
"""
import mediapipe as mp
import cv2


class HandDetector():
    # 初始化方法
    def __init__(self):
        self.hand_detector = mp.solutions.hands.Hands()
        # mp.solutions.drawing_utils用于绘制
        self.mp_drawing = mp.solutions.drawing_utils

    # 查找手部关键点
    def process(self, img):
        # 将图像转换为rgb显示   因为opencv的默认管道是gbr
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 存储手部关键点数据
        self.hand_data = self.hand_detector.process(img_rgb)
        # multi_hand_landmarks 表示手在图像中的位置

        if self.hand_data.multi_hand_landmarks:
            # 将手部的二十个节点遍历出来
            for landma in self.hand_data.multi_hand_landmarks:
                # 将点画出来   mp.solutions.hands.HAND_CONNECTIONS 将关节点用线连起来
                self.mp_drawing.draw_landmarks(img, landma, mp.solutions.hands.HAND_CONNECTIONS)

    # 找到21个点的位置坐标
    def find_postion(self, img):
        # cpencv .shape 函数返回的是图像的高度 宽度及色彩通道数
        h, w, c = img.shape
        # 定义位置字典
        postion = {"Left": {}, "Right": {}}
        # 判断是否存在手部关键点数据
        if self.hand_data.multi_hand_landmarks:
            i = 0
            for point in self.hand_data.multi_handedness:
                # 判断左右手
                score = point.classification[0].score
                if score >= 0.8:
                    label = point.classification[0].label
                    hand_lms = self.hand_data.multi_hand_landmarks[i].landmark
                    for id, lm in enumerate(hand_lms):
                        # print(lm)  lm 返回的数据是 该坐标在整张图片中的占比
                        x, y = float(lm.x * w * 1920/1080*2 ), float(lm.y * h* 1920/1080*2 )
                        postion[label][id] = (x, y)
                i = i + 1
        return postion

    # 判断手指是否伸直
    def check_finger(self, start_num, end_num, label, position):
        finger_start = position[label].get(start_num, None)
        finger_end = position[label].get(end_num, None)
        if finger_end and finger_start:
            check_num = finger_start[1] - finger_end[1]

            if check_num < 0:
                return True

    # 判断手指移动的距离
    def finger_distance(self,finger_num,label,position):
        finger = position[label].get(finger_num, None)
        if finger:
            return finger

    # 判断哪两个手指是否打开 finger_num1 finger_num2 两个不同的手指指尖,position 位置坐标
    def check_isMerge(self, finger_num1, finger_num2, label, position):
        finger1 = position[label].get(finger_num1, None)
        finger2 = position[label].get(finger_num2, None)
        if finger1 and finger2:
            check_num = finger2[0] - finger1[0]
            if check_num > 150:
                return True
