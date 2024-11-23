import time
import win_tool
from tkinter import messagebox
import dao2_common
import threading


# 草药6分钟刷一次
MAX_COUNT = 200

is_run = False
lock = threading.Lock()

# 1901
cao_name = "半夏"

# 每一轮休息
round_delay = 15


def gather(hwnd):
    print(f"{cao_name} gather={is_run}")
    t = threading.Thread(target=gather_cao, args=(hwnd,), daemon=True)
    t.start()


def gather_cao(hwnd):
    start_time = time.time()
    global is_run

    inx = 0
    counter = 0
    # 二维数组，第一个点 表示中转点
    position = ["455,1238", "526,1381", ["546,1345", "675,1405"], "841,1425", "1028,1326",
                "1249,1260", "1343,1230", "1408,1139"]
    position_delay = [11, 14, 12, 16, 16,
                      28, 11, 11]

    # 神仙索
    if not dao2_common.shen_xian_suo_ch_song(hwnd):
        dao2_common.say_hwnd(hwnd, "没找到神仙索！")
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

        if inx >= len(position):
            # 回原点
            inx = 0
            dao2_common.shen_xian_suo_ch_song(hwnd)
            time.sleep(10)
            if is_run is False:
                print("停止脚本")
                return
            win_tool.send_key_to_window_frequency(hwnd, "w", 3)
            time.sleep(3)

        # 导航
        pos = position[inx]
        pos_next = position[inx]
        if not isinstance(pos, str):
            on_xy = dao2_common.navigation_x_y(hwnd, pos[0])
            dao2_common.qi_ma(hwnd)
            time.sleep(5)
            pos_next = pos[1]

        on_xy = dao2_common.navigation_x_y(hwnd, pos_next)
        if isinstance(on_xy, str):
            messagebox.showwarning("警告", on_xy)
            return

        if is_run is False:
            print("停止脚本")
            return

        # 骑马
        if 6 < position_delay[inx]:
            dao2_common.qi_ma(hwnd)
        time.sleep(position_delay[inx])

        if is_finish:
            is_finish = False
            dao2_common.say_hwnd(hwnd, f"挖-草-{cao_name}- 完成一轮 挖到{counter} 点数{len(position)} 休息一会")
            time.sleep(round_delay)

        if is_run is False:
            print("停止脚本")
            return

        # 抬高相机
        dao2_common.camera_top(hwnd)
        time.sleep(0.3)
        inx += 1

        # 找、挖
        dh_count = 0
        while is_run:
            dh_xy = dao2_common.find_wu_ban_xia_list(hwnd)
            if None is dh_xy:
                print(f"没找到{cao_name}")
                # 挖没了，打断
                break
            if dh_count > 6:
                print(f"{cao_name}单个点位挖超量，可能识图出问题")
                break

            if dh_xy[0] > 2000:
                continue

            dao2_common.wa_cao(hwnd, dh_xy)
            counter += 1
            dh_count += 1
            print(f"dh_count={dh_count}, counter={counter}")

        if inx >= len(position):
            # 一轮完成 回到最早位置
            is_finish = True
        dao2_common.activity_window(hwnd)

    # 结束
    is_run = False
    dao2_common.say_hwnd(hwnd, f"挖{cao_name}完成耗时={time.time() - start_time}s")