import time
import win_tool
import bg_find_pic_area
import threading
from tkinter import messagebox
import dao2_common
import traceback
import threading
from datetime import datetime
import log3

# 草药6分钟刷一次

w, h = win_tool.get_win_w_h()

is_run = False
lock = threading.Lock()

def gather(hwnd):
    print(f"gather_gan_cao gather={is_run}")
    t = threading.Thread(target=gather_gan_cao, args=(hwnd,), daemon=True)
    t.start()


def gather_gan_cao(hwnd):
    start_time = time.time()
    global is_run
    # 激活窗口
    # win_tool.activate_window(hwnd)
    # time.sleep(0.1)

    inx = 0
    max_count = 170
    counter = 0
    # 下标 5 开始是朝歌的点
    zhao_ge_inx = 5
    position = ["646,849", "642,940", "645,958", "688,1052", "790,1057",
                "719,1181", "726,1253", "641,1304", "528,1316", "498,1353"]
    position_delay = [10, 9, 5, 15, 8,
                      55, 9, 16, 31, 7]

    # 土遁去碎木
    is_ok = ""
    try:
        is_ok = dao2_common.tu_dun_sui_mu(hwnd)
    except Exception as e:
        print(f"发生异常：{e}")
        is_ok = traceback.format_exc()

    if "" != is_ok:
        is_run = False
        messagebox.showwarning("警告", is_ok)
        return
    time.sleep(10)
    if is_run is False:
        print("停止脚本")
        return
    win_tool.send_key_to_window_frequency(hwnd, "w", 3)
    time.sleep(1)

    is_finish = False

    while counter < max_count:

        if is_run is False:
            print("停止脚本")
            return

        if inx >= len(position):
            inx = 0
            # 回碎木
            dao2_common.tu_dun_sui_mu(hwnd)
            time.sleep(9)
            if is_run is False:
                print("停止脚本")
                return
            # win_tool.send_key("w", 3)
            win_tool.send_key_to_window_frequency(hwnd, "w", 3)
            time.sleep(1)

        if inx == zhao_ge_inx:
            # 去朝歌
            dao2_common.tu_dun_zhao_ge(hwnd)
            time.sleep(9)
            if is_run is False:
                print("停止脚本")
                return
            # win_tool.send_key("w", 3)
            win_tool.send_key_to_window_frequency(hwnd, "w", 3)
            time.sleep(1)

        # 导航
        on_xy = dao2_common.navigation_x_y(hwnd, position[inx])
        if isinstance(on_xy, str):
            messagebox.showwarning("警告", on_xy)
            return

        if is_run is False:
            print("停止脚本")
            return

        # 骑马
        dao2_common.qi_ma(hwnd)
        time.sleep(position_delay[inx])

        if is_finish:
            is_finish = False
            dao2_common.say_hwnd(hwnd, f"挖-草- 完成一轮 挖到{counter} 点数{len(position)}")
            # time.sleep(1)

        if is_run is False:
            print("停止脚本")
            return

        # 抬高相机
        dao2_common.camera_top(hwnd)
        time.sleep(0.2)
        inx += 1

        # 找、挖
        dh_count = 0
        while True:

            if is_run is False:
                print("停止脚本")
                return

            dh_xy = dao2_common.find_gan_cao_list(hwnd)
            if None is dh_xy:
                print("没找到甘草")
                # 挖没了，打断
                break
            if dh_count > 6:
                print("甘草单个点位挖超量，可能识图出问题")
                break

            if dh_xy[0] > 2000:
                continue

            # win_tool.move_mouse(dh_xy[0] + 4, dh_xy[1] + 8)
            # time.sleep(0.1)
            # win_tool.mouse_left_click()
            dao2_common.wa_cao(hwnd, dh_xy)
            counter += 1
            dh_count += 1

        if inx >= len(position):
            # 一轮完成 回到最早位置
            is_finish = True
        dao2_common.activity_window(hwnd)

    # 结束
    is_run = False
    dao2_common.say_hwnd(hwnd, f"挖甘草完成耗时={time.time() - start_time}s")
    # messagebox.showwarning("通知", f"挖甘草完成耗时={time.time() - start_time}s")
