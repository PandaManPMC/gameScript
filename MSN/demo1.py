import random
import time

import win32con
import win32gui

import win_tool
import win32api
import bg_find_pic_area
import cv2
import numpy as np



def test_msn():
    window_name = "MapleStory N"
    window_handles = win_tool.get_all_window_handles_by_name(window_name)
    print(window_handles)
    hwnd = window_handles[0]

    # w,h = win_tool.get_win_w_h()
    # scale = win_tool.get_screen_scale(hwnd)
    # w = int(w/scale)
    # h = int(h/scale)
    # w = None
    # h = None
    w = 1383
    h = 815

    x_of = int(w*0.4)
    # y_of = int(h*0.85) + 65
    y_of = int(h*0.85)
    # bh = h
    bh = h - 40

    screen_img = bg_find_pic_area.capture_window(hwnd, x_of, y_of, int(w*0.6), bh)
    cv2.imshow("Result", np.array(screen_img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # template_img_path = "./img/mp.bmp"
    template_img_path = "./img/hp.bmp"

    xy = bg_find_pic_area.find_image(hwnd, template_img_path, x_of, y_of, int(w*0.6), bh, 0.85)
    print(xy)
    if None is xy:
        return
    win_tool.activate_window(hwnd)
    win_tool.move_mouse(xy[0], xy[1])


def test_d2():
    window_name = "刀剑2"
    window_handles = win_tool.get_all_window_handles_by_name(window_name)
    print(window_handles)
    hwnd = window_handles[0]

    w, h = win_tool.get_win_w_h()
    x_of = int(w*0.4)
    y_of = int(h*0.2)
    c_w = int(w*0.75)
    c_h = int(h*0.75)

    screen_img = bg_find_pic_area.capture_window(hwnd, x_of, y_of, c_w, c_h)
    cv2.imshow("Result", np.array(screen_img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    time.sleep(1)

    template_img_path = "./img/demo.bmp"  # 替换为你要匹配的模板图片路径
    xy = bg_find_pic_area.find_image(hwnd, template_img_path, x_of, y_of, c_w, c_h, 0.85)
    print(xy)
    if None is xy:
        return
    win_tool.activate_window(hwnd)
    win_tool.move_mouse(xy[0], xy[1])


if __name__ == "__main__":
    test_msn()
    # test_d2()
    rand_num = random.gauss(0.1, 0.2)  # 均值 0，标准差 1
    print(rand_num)
    print(round(abs(rand_num), 3))
    rand_num = random.betavariate(2, 5)
    print(rand_num)