import time
import win_tool
import threading
from tkinter import messagebox
import dao2_common
import traceback
from datetime import datetime

is_run = False
lock = threading.Lock()

MAX_COUNT = 200

cao_name = "辉铜矿"


def wa(hwnd):
    start_time = time.time()
    global is_run

    inx = 0
    counter = 0
    position = ["684,1363", "705,1435", "697,1474", "754,1503", "788,1469",
                "832,1439", "828,1405", "843,1305", "856,1254", "946,1217"]
    position_delay = [5, 16, 10, 13, 14, 10, 9, 31, 11, 24]

    # 神仙索
    if not dao2_common.shen_xian_suo_ch_song(hwnd):
        dao2_common.say_hwnd(hwnd, "没找到神仙索 679,1359 ！")
        is_run = False
        return
    time.sleep(10)
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

        sleep = 0
        if inx >= len(position):
            inx = 0

            sleep = 40
            if is_run is False:
                print("停止脚本")
                return
        else:
            sleep = position_delay[inx]

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
        time.sleep(sleep)

        if is_finish:
            is_finish = False
            dao2_common.say_hwnd(hwnd, f"挖-草-{cao_name} 完成一轮 挖到{counter} 点数{len(position)}")

        if is_run is False:
            print("停止脚本")
            return

        # 抬高相机
        dao2_common.camera_top(hwnd)
        time.sleep(0.3)
        inx += 1

        # 找大黄、挖大黄
        dh_count = 0
        while is_run:

            dh_xy = dao2_common.find_hui_tong_kuang_list(hwnd)
            if None is dh_xy:
                print(f"没找到{cao_name}")
                # 大黄挖没了，打断
                break
            if dh_count > 6:
                print(f"{cao_name}单个点位挖超量，可能识图出问题")
                break

            # win_tool.move_mouse(dh_xy[0] + 4, dh_xy[1] + 8)
            # time.sleep(0.1)
            # win_tool.mouse_left_click()
            # time.sleep(6)
            dao2_common.wa_cao(hwnd, dh_xy)
            counter += 1
            dh_count += 1

        if inx >= len(position):
            # 一轮完成 回到最早位置
            is_finish = True

    # 结束
    is_run = False
    dao2_common.say_hwnd(hwnd, f"挖{cao_name}完成耗时={time.time() - start_time}s")
    # messagebox.showwarning("通知", f"挖大黄完成 耗时={time.time() - start_time}s")


def gather(hwnd):
    print(f"{cao_name}={is_run}")
    t = threading.Thread(target=wa, args=(hwnd,), daemon=True)
    t.start()

