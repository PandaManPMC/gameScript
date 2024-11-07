import time

import cv2
from paddleocr import PaddleOCR
import matplotlib.pyplot as plt
import win_tool
import bg_find_pic_area
import numpy as np
import dao2_common
import py_tool
import os
import paddleocr
paddleocr_path = os.path.dirname(paddleocr.__file__)
print(f"PaddleOCR 的路径: {paddleocr_path}")
# D:\a\codes\game_script\pythonProject\.venv\lib\site-packages\paddleocr


# window_name = "夏禹剑 - 刀剑2"
# hwnd = win_tool.get_window_handle(window_name)
#
# w,h = win_tool.get_win_w_h()
# image = bg_find_pic_area.capture_window(hwnd, int(w*0.2), 0, int(w*0.75), int(h * 0.7))
#
# # 1. 读取图片
# # image = cv2.imread(image_path)
#
# # 2. 转为灰度图
# gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
#
# # 6. 使用 PaddleOCR 进行中文识别
# ocr = PaddleOCR(use_angle_cls=True, lang='ch')
# result = ocr.ocr(gray_image, cls=True)
#
# # 7. 输出识别结果
# resu = ""
# print("识别结果:")
# for line in result[0]:
#     print(f"文字: {line[1][0]}, 置信度: {line[1][1]:.2f}")
#     resu = resu + line[1][0]
#
# print(resu)
# substring = resu
# start = resu.find("成长等级：")
# if start != -1:
#     substring = resu[start:start+8:1]
#     print(start)
#
# l_i = py_tool.rfind_digit_inx(substring)
# l_i = l_i if l_i == len(substring) else l_i + 1
# substring = substring[0:l_i]
#
# print(substring)
#
# win_tool.send_mouse_right_click(hwnd, int(w*0.5), int(h*0.5))
# time.sleep(0.5)
# dao2_common.say_hwnd(hwnd, substring)
# time.sleep(1)
