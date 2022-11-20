"""
作者：zwq
日期:2022年01月23日
"""

import cv2
import pyautogui as py
import time

# 引入自己编写的类方法
from handUtils import HandDetector

# 视频捕捉 0为默认摄像头
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
hand_detector = HandDetector()

# 当前屏幕尺寸 以后可匹配不同设备在做优化
# print(py.size())

# success自己定义的变量 用来储存返回的值 即是否读取成功  img为每一帧的图片
while True:
    success, img = camera.read()
    if success:
        # 镜像反转
        img = cv2.flip(img, 1)
        hand_detector.process(img)
        # 获取图像中的手指坐标
        position = hand_detector.find_postion(img)

        # 判断食指是否伸出
        finger2 = hand_detector.check_finger(8, 5, 'Right', position)
        # 判断中指是否伸出
        finger3 = hand_detector.check_finger(12, 9, 'Right', position)
        # 如果伸出食指

        if finger2 and finger3 != True:
            # 获取当前食指坐标点
            result = hand_detector.finger_distance(8, "Right", position)
            py.moveTo(int(result[0]), int(result[1]), duration=0.05)

        if finger2 and finger3:
            # 判断食指和中指是否打开
            checkOpen = hand_detector.check_isMerge(8, 12, "Right", position)
            if checkOpen:
                py.click(clicks=1)

        # 如果读取成功 将其设置在cv2创建的窗口上  窗口名称叫Videos  可自行设置
        cv2.imshow('Video', img)
    # 等待按键
    k = cv2.waitKey(1)
    # 判断是否按了q键
    if k == ord('q'):
        break

# 释放摄像头
camera.release()
# 关掉所有的创建的窗口
cv2.destroyAllWindows()
