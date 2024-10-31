import time

import bg_find_pic
import bg_find_pic_area
import win_tool
import dao2_common

w, h = win_tool.get_win_w_h()


def test_scale():
    window_name = "夏禹剑 - 刀剑2"
    hwnd = win_tool.get_window_handle(window_name)
    xy = dao2_common.find_pic(hwnd, "img/6oclock_dialog_close.bmp", 0, 0, w, h, 0.8)


def test_desktop():
    hwnd = desktop_handle = win_tool.get_desktop_window_handle()
    # xy = dao2_common.find_pic(hwnd, "img/6oclock_dialog_close.bmp", 0, 0, w, h, 0.8, True)
    dao2_common.close_tong_zhi()


def test_find_nu():
    hwnd = win_tool.get_window_handle("夏禹剑 - 刀剑2")
    # xy = dao2_common.find_pic(hwnd, "img/nu1.bmp", int(w * 0.3), int(h * 0.6), int(w * 0.9), h - 50, 0.8)
    xy = dao2_common.find_pic(hwnd, "img/qiongyun_luwushuang.bmp", 400, 200, w - 400, int(h * 0.8))


def find_img(img_name):
    window_name = "夏禹剑 - 刀剑2"
    hwnd = win_tool.get_window_handle(window_name)
    xy = dao2_common.find_pic(hwnd, img_name, 500, 0, w - 50, int(h * 0.3))
    win_tool.move_mouse(xy[0], xy[1])


if __name__ == "__main__":
    print(f"w={w},h={h}")
    # test_scale()
    # test_desktop()
    # test_find_nu()
    # find_img("img/jingjichang.bmp")

    hwnd = win_tool.get_window_handle("夏禹剑 - 刀剑2")
    # xy = dao2_common.find_pic(hwnd, "img/nu1.bmp", int(w * 0.3), int(h * 0.5), int(w * 0.5),
    #                           h, 0.7)
    # print(xy)

    # dao2_common.say_hwnd(hwnd, f"有怒气，放怒气技能 {hwnd}")

    # dao2_common.say_hwnd(hwnd, f"asdc")

    # win_tool.send_key_to_window(hwnd, "w", 1)
    # win_tool.send_key_to_window_frequency(hwnd, "w", 3)

    # win_tool.send_key_to_window(hwnd, "enter", 1)
    # xy = dao2_common.find_pic(hwnd, "img/jingjichang_duanweisai.bmp", 0, 0, w,
    #                           h, 0.7)
    # xy = dao2_common.find_pic(hwnd, "img/jingjichang_duanweisai.bmp", int(w * 0.2), int(h * 0.1), int(w * 0.7),
    #                           int(h * 0.5), 0.7)
    xy = dao2_common.find_pic(hwnd, "img/cangku_linlangge.bmp", int(w * 0.2), int(h * 0.5), int(w*0.75), h-100)

    print(xy)

