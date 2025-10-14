import time

import numpy as np
import win32gui

import gamelib
import cv2

from gamelib import win_tool

print(cv2.__version__)


def test():
    w,h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name("37山河图志")
    print(window_handles)
    hwnd = window_handles[0]

    # hwnd = gamelib.win_tool.get_desktop_window_handle()
    # screen_img = gamelib.bg_find_pic_area.capture_window(hwnd, 500, 500, w-100, h - 50)
    # cv2.imshow("Result", np.array(screen_img))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    screen_img = gamelib.find_pic.capture_window_area(hwnd, 100, 200, w,h)
    cv2.imshow("Result", np.array(screen_img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # test()

    w,h = gamelib.win_tool.get_win_w_h()
    # 示例：查找 Chrome 窗口中的图片
    window_handles = gamelib.win_tool.get_all_window_handles_by_name("37山河图志")
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        exit(0)

    location = gamelib.find_pic.find_image_in_window(hwnd, "./img/jineng5.png",300,500,w,h, threshold=0.85, debug=True)
    print(location)
    win_tool.activate_window(hwnd)
    time.sleep(1)
    win_tool.move_mouse(location[0],location[1])
