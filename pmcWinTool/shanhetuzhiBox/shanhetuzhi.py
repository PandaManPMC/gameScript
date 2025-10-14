import time

import gamelib
from MSN import win_tool

is_run_auto_zhenyingzhan = False
is_run_auto_longzhuashou = False

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
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/jineng5.png", 300, 500, w, h, threshold=0.85,
                                                         debug=False)
        if location is None:
            time.sleep(1)
            continue

        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(5)


def run_auto_longzhuashou():
    w, h = gamelib.win_tool.get_win_w_h()
    # 示例：查找 Chrome 窗口中的图片
    window_handles = gamelib.win_tool.get_all_window_handles_by_name("37山河图志")
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return

    global is_run_auto_longzhuashou
    while is_run_auto_longzhuashou:
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/jineng5.png", 300, 500, w, h, threshold=0.85,
                                                         debug=False)
        if location is None:
            time.sleep(10)
            continue

        # win_tool.send_key_to_window(hwnd, "5") # chrome 无法后台发送按键
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(10)
