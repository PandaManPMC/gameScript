import time
import win_tool
import bg_find_pic_area
import threading
from tkinter import messagebox
import dao2_common
import traceback
import threading
from datetime import datetime

# 草药6分钟刷一次
MAX_COUNT = 200

is_run = False
lock = threading.Lock()


def gather(hwnd):
    print(f"gather_cao_yao gather={is_run}")
    t = threading.Thread(target=gather_cao_yao, args=(hwnd,), daemon=True)
    t.start()


def gather_cao_yao(hwnd):
    start_time = time.time()
    global is_run
    # 激活窗口
    win_tool.activate_window(hwnd)
    time.sleep(0.1)

    inx = 0
    counter = 0
    position = ["1340,1182", "1428,1146", "1426,1182", "1393,1266", "1504,1353",
                "1579,1343", "1536,1237", "1500,1175", "1533,1126", "1668,1125"]
    position_delay = [11, 10, 15, 12, 11,
                      7, 9, 8, 6, 12]

    # 朝歌
    try:
        is_ok = dao2_common.tu_dun_zhao_ge(hwnd)
    except Exception as e:
        print(f"发生异常：{e}")
        is_ok = traceback.format_exc()

    if "" != is_ok:
        is_run = False
        messagebox.showwarning("警告", is_ok)
        return
    time.sleep(7)
    if is_run is False:
        print("停止脚本")
        return
    win_tool.send_key_to_window_frequency(hwnd, "w", 3)
    time.sleep(3)

    is_finish = False

    while counter < MAX_COUNT:

        if is_run is False:
            print("停止脚本")
            return

        if inx >= len(position):
            inx = 0
            # 去朝歌
            dao2_common.tu_dun_zhao_ge(hwnd)
            time.sleep(7)
            if is_run is False:
                print("停止脚本")
                return
            win_tool.send_key_to_window_frequency(hwnd, "w", 3)
            time.sleep(3)

        # 导航
        # 这个点回往城里走,先去中转 1364,1179
        if "1428,1146" == position[inx]:
            on_xy = dao2_common.navigation_x_y(hwnd, "1364,1179")
            if isinstance(on_xy, str):
                messagebox.showwarning("警告", on_xy)
                return
            time.sleep(3)

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
        inx += 1

        # 找、挖
        dh_count = 0
        while is_run:

            dh_xy = dao2_common.find_ma_huang_list(hwnd)
            if None is dh_xy:
                print("没找到甘草")
                # 挖没了，打断
                break
            if dh_count > 6:
                print("单个点位挖超量，可能识图出问题")
                break

            if dh_xy[0] > 2000:
                continue

            # win_tool.move_mouse(dh_xy[0] + 4, dh_xy[1] + 8)
            # time.sleep(0.3)
            # win_tool.mouse_left_click()
            # time.sleep(6)
            dao2_common.wa_cao(hwnd, dh_xy)
            counter += 1
            dh_count += 1

        if inx >= len(position):
            # 一轮完成 回到最早位置
            is_finish = True
        dao2_common.activity_window(hwnd)

    # 结束
    is_run = False
    dao2_common.say_hwnd(hwnd, f"挖麻黄完成耗时={time.time() - start_time}s")
    # messagebox.showwarning("通知", f"挖麻黄完成耗时={time.time() - start_time}s")
