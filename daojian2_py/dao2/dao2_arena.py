import win_tool
import threading
import time
import dao2_common
import traceback
from tkinter import messagebox
import log3

w, h = win_tool.get_win_w_h()

is_run = False
lock = threading.Lock()


def start_arena(hwnd_array):
    global is_run
    with lock:
        if is_run:
            # 每个窗口句柄 开启一个线程
            for hwnd in hwnd_array:
                t = threading.Thread(target=arena, args=(hwnd,), daemon=True)
                t.start()


def arena(hwnd):
    # 技能 每 1s 按一个，检测到有怒气时发动快捷键 5
    skill_arr = ["1", "2", "3", "4", "6", "7", "8", "9", "0", "-"]
    global is_run
    while is_run:
        # 在队列判断
        is_queue = False
        is_fu_ben = False
        xy = dao2_common.find_pic(hwnd, "img/jingjichang_paidui.bmp", int(w * 0.7), int(h * 0.6), w - 10, h - 50, 0.8)
        if None is not xy:
            is_queue = True

        # 在副本判断
        xy = dao2_common.find_pic(hwnd, "img/jingjichang_fuben.bmp", int(w * 0.7), int(h * 0.6), w - 10, h - 50, 0.8)
        if None is not xy:
            is_fu_ben = True

        # 不在队列，也不在副本，加锁激活窗口加入排队
        if not is_queue and not is_fu_ben:
            arena_queue(hwnd)

        # 已经在副本，开始攻击
        if is_fu_ben:
            time.sleep(19)
            # dao2_common.say_hwnd(hwnd, f"{hwnd} 检测到已经在副本")

            camera_forward(hwnd)

            nu = 0
            while is_run:
                win_tool.send_key_to_window(hwnd, "tab")
                nu += 1
                for i in range(len(skill_arr)):
                    print(f"攻击 {skill_arr[i]}")
                    if i != 0 and i % 6 == 0:
                        win_tool.send_key_to_window_frequency(hwnd, "w", 3)
                        time.sleep(0.5)
                    win_tool.send_key_to_window(hwnd, skill_arr[i])
                    time.sleep(1)
                # if 0 != nu and nu % 2 == 0:
                    # 检查怒气
                    # xy = dao2_common.find_pic(hwnd, "img/nu1.bmp", int(w * 0.3), int(h * 0.5), int(w * 0.5),
                    #                           h, 0.7)
                    # if None is not xy:
                win_tool.send_key_to_window_frequency(hwnd, "w", 3)
                time.sleep(0.5)
                # 有怒气，按 5
                win_tool.send_key_to_window(hwnd, "5")
                    # dao2_common.say_hwnd(hwnd, f"有怒气，放怒气技能 {hwnd}")

                # 在副本判断
                xy = dao2_common.find_pic(hwnd, "img/jingjichang_fuben.bmp", int(w * 0.7), int(h * 0.6), w - 10, h - 50,
                                          0.8)
                if None is xy:
                    # 不在副本，打断循环
                    break
        else:
            time.sleep(2)


def camera_forward(hwnd):
    with lock:
        win_tool.activate_window(hwnd)
        time.sleep(0.3)
        # 摆正相机
        dao2_common.camera_forward(hwnd)
        time.sleep(1)
        # 向前走
        win_tool.send_key_to_window(hwnd, "w", 3)


def arena_queue(hwnd):
    with lock:
        # 先查一下，竞技场按钮不存在，说明正在进入，则不激活窗口 直接退出
        xy_jj = dao2_common.find_pic(hwnd, "img/jingjichang.bmp", int(w * 0.6), 0, w - 10, int(h * 0.3), 0.8)
        if None is xy_jj:
            log3.logger.debug(f"arena_queue {hwnd} 竞技场按钮不存在")
            return
        # 不在队列，也不在副本，加锁激活窗口加入排队
        win_tool.activate_window(hwnd)
        time.sleep(0.3)

        # 点击竞技场
        win_tool.send_input_mouse_left_click(xy_jj[0] + 11, xy_jj[1] + 11)
        time.sleep(0.3)

        # 点击段位赛
        # d_w = False
        for i in range(3):
            xy = dao2_common.find_pic(hwnd, "img/jingjichang_duanweisai.bmp", int(w * 0.2), int(h * 0.1), int(w * 0.8), int(h * 0.6), 0.7)
            if None is xy:
                time.sleep(0.2)
                continue
            win_tool.send_input_mouse_left_click(xy[0] + 8, xy[1] + 8)
            time.sleep(0.3)
            d_w = True
            break
        # if not d_w:
        #     print("没找到段位赛 jingjichang_duanweisai")
        #     return

        # 点击 报名
        xy = dao2_common.find_pic(hwnd, "img/jingjichang_baomingcanjia.bmp", int(w * 0.2), int(h * 0.4), int(w * 0.7), int(h * 0.7), 0.8)
        if None is xy:
            return

        win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
        time.sleep(0.3)

        # 关闭, 再次点击竞技场
        win_tool.send_input_mouse_left_click(xy_jj[0] + 5, xy_jj[1] + 5)
        time.sleep(0.3)

        dao2_common.say(f"{hwnd} 完成段位赛报名")

