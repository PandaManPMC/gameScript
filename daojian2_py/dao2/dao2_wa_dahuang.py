import time
import win_tool
import threading
from tkinter import messagebox
import dao2_common
import traceback
from datetime import datetime

is_run = False
lock = threading.Lock()


def wa(hwnd):
    start_time = time.time()
    global is_run
    # 激活窗口
    win_tool.activate_window(hwnd)
    time.sleep(0.1)

    inx = 0
    max_count = 165
    counter = 0
    # 下标 8 开始是朝歌的点
    zhao_ge_inx = 8
    position = ["638,900", "642,930", "657,980", "698,999", "706,1051", "771,1049", "809,1069", "821,1151",
                "1085,1289", "1067,1240", "1100,1234", "1023,1315", "995,1351", "976,1318", "914,1150"]
    position_delay = [10, 6, 7, 7, 11, 8, 6, 11,
                      26, 8, 5, 9, 6, 6, 19]

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
    win_tool.send_key("w", 3)
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
            win_tool.send_key("w", 3)
            time.sleep(1)

        if inx == zhao_ge_inx:
            # 去朝歌
            dao2_common.tu_dun_zhao_ge(hwnd)
            time.sleep(9)
            if is_run is False:
                print("停止脚本")
                return
            win_tool.send_key("w", 3)
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
            print(f"挖-草- 完成一轮 挖到{counter} 点数{len(position)}")
            dao2_common.say(f"挖-草- 完成一轮 挖到{counter} 点数{len(position)}")


        if is_run is False:
            print("停止脚本")
            return

        # 抬高相机
        dao2_common.camera_top()
        inx += 1

        # 找大黄、挖大黄
        dh_count = 0
        while True:

            if is_run is False:
                print("停止脚本")
                return

            dh_xy = dao2_common.find_da_huang_list(hwnd)
            if None is dh_xy:
                print("没找到大黄")
                # 大黄挖没了，打断
                break
            if dh_count > 6:
                print("大黄单个点位挖超量，可能识图出问题")
                break

            win_tool.move_mouse(dh_xy[0] + 4, dh_xy[1] + 8)
            time.sleep(0.1)
            win_tool.mouse_left_click()
            time.sleep(6)
            counter += 1
            dh_count += 1

        if inx >= len(position):
            # 一轮完成 回到最早位置
            is_finish = True
    # sz_xy = dao2_common.find_lvse_shouzhang(hwnd)
    # if None is sz_xy:
    #     print("没有找到手掌")

    # 结束
    is_run = False
    dao2_common.say(f"挖大黄完成耗时={time.time() - start_time}s")
    messagebox.showwarning("通知", f"挖大黄完成 耗时={time.time() - start_time}s")


def wa_da_huang(hwnd):
    print(f"wa_da_huang={is_run}")
    t = threading.Thread(target=wa, args=(hwnd,), daemon=True)
    t.start()

