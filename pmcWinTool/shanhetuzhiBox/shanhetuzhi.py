import time

import gamelib
from MSN import win_tool

is_run_auto_zhenyingzhan = False
is_run_auto_longzhuashou = False
is_run_auto_xianqi = False


def run_auto_zhenyingzhan():
    w, h = gamelib.win_tool.get_win_w_h()
    # 示例：查找 Chrome 窗口中的图片
    window_handles = gamelib.win_tool.get_all_window_handles_by_name("37山河图志")
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return

    global is_run_auto_zhenyingzhan
    while is_run_auto_zhenyingzhan:
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/lijifuhuo.png",  w*0.15, h*0.2, w*0.9, h, threshold=0.9,
                                                         debug=False)
        if location is None:
            time.sleep(1)
            continue

        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(3)


def run_auto_longzhuashou():
    w, h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name("37山河图志")
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return

    global is_run_auto_longzhuashou
    while is_run_auto_longzhuashou:
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/jineng5.png", w*0.15, h*0.5, w*0.95, h, threshold=0.95,
                                                         debug=False)
        if location is None:
            time.sleep(3)
            continue

        # win_tool.send_key_to_window(hwnd, "5") # chrome 无法后台发送按键
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(1)
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(10)


def run_auto_xianqi():
    w, h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name("37山河图志")
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return

    global is_run_auto_xianqi
    while is_run_auto_xianqi:
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/anquanfuhuo.png", w*0.2, h*0.15, w*0.8, h*0.85, 0.95, False)
        if location is None:
            time.sleep(2)
            continue
        # 复活
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(2)
        # 找跨服战场
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/kuafuzhanchan.png", w*0.5, 0, w, h*0.6, 0.95, False)
        if location is None:
            time.sleep(2)
            continue
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(1)
        # 找仙骑
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/xianqi.png", w*0.5, 0, w, h*0.8, 0.95, False)
        if location is None:
            time.sleep(2)
            continue
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(1)
        # 前往挑战
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/qianwangtiaozhan.png", w*0.5, h*0.1, w, h*0.8, 0.95, False)
        if location is None:
            time.sleep(2)
            continue
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(1)