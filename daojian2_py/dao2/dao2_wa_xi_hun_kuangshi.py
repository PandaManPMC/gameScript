import time
import win_tool
from tkinter import messagebox
import dao2_common
import threading

w,h = win_tool.get_win_w_h()

MAX_COUNT = 150

is_run = False
lock = threading.Lock()

# 栖魂矿石
cao_name = "栖魂矿石"


def gather(hwnd):
    print(f"dao2_wa_baishu gather={is_run}")
    t = threading.Thread(target=gather_cao, args=(hwnd,), daemon=True)
    t.start()


def gather_cao(hwnd):
    start_time = time.time()
    global is_run

    inx = 0
    counter = 0
    # 二维数组，第一个点 表示中转点
    position = ["361,220", "368,192", "372,177", "391,175",
                "433,166", "453,163", "492,222"]

    # 去鸟山
    dao2_common.tu_dun_niao_shan(hwnd)
    time.sleep(7)
    if is_run is False:
        print("停止脚本")
        return
    win_tool.send_key_to_window_frequency(hwnd, "w", 3)
    time.sleep(3)

    dao2_common.camera_focus(360)

    is_finish = False
    is_sec = True

    while counter < MAX_COUNT:

        if is_run is False:
            print("停止脚本")
            return

        if inx >= len(position) and is_sec:
            is_sec = False
            inx -= 2
        elif 0 == inx and not is_sec:
            is_sec = True

        # 导航
        pos = position[inx]
        pos_next = position[inx]
        if not isinstance(pos, str):
            on_xy = dao2_common.navigation_x_y(hwnd, pos[0])
            time.sleep(1.5)
            pos_next = pos[1]

        on_xy = dao2_common.navigation_x_y(hwnd, pos_next)
        if isinstance(on_xy, str):
            messagebox.showwarning("警告", on_xy)
            return

        if is_run is False:
            print("停止脚本")
            return

        # 骑马
        dao2_common.qi_ma(hwnd)
        time.sleep(5)

        if is_finish:
            is_finish = False
            dao2_common.say_hwnd(hwnd, f"挖{cao_name}- 完成一轮 挖到{counter} 点数{len(position)} 休息一会")
            time.sleep(1)

        if is_run is False:
            print("停止脚本")
            return

        if is_sec:
            inx += 1
        else:
            inx -= 1

        # 找、挖
        dh_count = 0
        non_count = 0
        while is_run:
            dao2_common.camera_forward(hwnd)
            time.sleep(0.3)

            dh_xy = dao2_common.find_cao_list(hwnd, [
                "img/xihunkuangshi1.bmp",
                "img/xihunkuangshi2.bmp",
                "img/xihunkuangshi3.bmp",])

            if None is dh_xy:
                print(f"没找到{cao_name}")
                non_count += 1
                if non_count < 4:
                    time.sleep(1)
                    continue
                # 挖没了，打断
                break
            if dh_count > 6:
                print(f"{cao_name}单个点位挖超量，可能识图出问题")
                break

            if dh_xy[0] > 2000:
                continue

            k_xy = [dh_xy[0], dh_xy[1] + 5]

            if win_tool.is_window_foreground(hwnd):
                win_tool.send_mouse_left_click(hwnd, k_xy[0] + 4, k_xy[1] + 8)
                time.sleep(5.7)
                return
            time.sleep(0.05)
            dao2_common.open_navigation_and_click(hwnd)
            time.sleep(0.05)
            win_tool.move_mouse_to(hwnd, k_xy[0] + 4, k_xy[1] + 8)
            time.sleep(0.05)
            win_tool.send_mouse_left_click(hwnd, k_xy[0] + 4, k_xy[1] + 8)
            time.sleep(0.1)

            if dont_attack(hwnd):
                win_tool.send_key_to_window_frequency(hwnd, "w", 3)
                time.sleep(0.6)
                dao2_common.esc_and_back(hwnd)
                time.sleep(0.05)
                dao2_common.esc_and_back(hwnd)
                continue

            win_tool.send_mouse_left_click(hwnd, k_xy[0] + 4, k_xy[1] + 8)
            time.sleep(5.8)

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

    # 去瓦当
    dao2_common.tu_dun_wa_dang(hwnd)
    time.sleep(7)
    if is_run is False:
        print("停止脚本")
        return
    win_tool.send_key_to_window_frequency(hwnd, "w", 3)
    time.sleep(3)


def dont_attack(hwnd):
    xy = dao2_common.find_pic(hwnd, "img/diren_xuetiao.bmp", int(w * 0.25), 0, int(w * 0.75), int(h * 0.2), 0.8)
    if None is xy:
        return False
    return True
