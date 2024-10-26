import win_tool
import threading
import time
import dao2_common
import traceback
from tkinter import messagebox

w, h = win_tool.get_win_w_h()

is_run_receive_notify = False
lock = threading.Lock()


# 接通知
# 1.多窗口接任务共享
# 2.多窗口接穿云箭
# 3.多窗口进副本
# 4.自动组队
def receive_notify(hwnd_array):
    t = threading.Thread(target=running_receive_notify, args=(hwnd_array,), daemon=True)
    t.start()


def running_receive_notify(hwnd_array):
    global is_run_receive_notify
    print(f"start_receive_notify hwnd_array={hwnd_array}")

    if None is hwnd_array:
        messagebox.showwarning("警告", "未找到 刀剑2 窗口")
        is_run_receive_notify = False

    hwnds  = win_tool.get_all_window_handles_by_name("刀剑2")
    print(f"hwnds={hwnds}")

    # 不断循环，检测
    while is_run_receive_notify:

        if is_run_receive_notify is False:
            print("脚本停止")
            return
        is_re = False
        for hwnd in hwnd_array:
            # 找 感叹号
            xy = dao2_common.find_pic(hwnd, "img/tongzhi_gantanhao.bmp", 400, 200, w - 500, int(h * 0.8))
            if None is xy:
                print(f"{hwnd} 未找到 tongzhi_gantanhao")
                time.sleep(0.1)
                continue

            # 找到，激活窗口，点击
            win_tool.activate_window(hwnd)
            time.sleep(0.15)
            win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)

            is_re = True
            time.sleep(0.1)
            # 找 勾
            xy = dao2_common.find_pic(hwnd, "img/sharerenwu_gou.bmp", 400, 400, w - 500, int(h * 0.7))
            if None is not xy:
                win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)
                time.sleep(0.1)
                continue

            xy = dao2_common.find_pic(hwnd, "img/chuangsong_tongyi.bmp", 400, 400, w - 500, int(h * 0.7))
            if None is not xy:
                win_tool.send_input_mouse_left_click(xy[0] + 8, xy[1] + 7)
                time.sleep(0.1)
                continue

        if 0 != len(hwnds):
            if is_re:
                win_tool.activate_window(hwnds[0])

