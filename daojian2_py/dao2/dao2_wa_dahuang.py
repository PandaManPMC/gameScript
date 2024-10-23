import time

import win_tool
import bg_find_pic_area
import threading
from tkinter import messagebox
import dao2_common
import traceback

is_run_wa_da_huang = False


def wa(hwnd):
    global  is_run_wa_da_huang
    # 激活窗口
    win_tool.activate_window(hwnd)
    time.sleep(0.1)

    inx = 0
    max_count = 165
    counter = 0
    position = ["638,900", "642,930", "657,980", "698,999", "706,1051", "771,1049", "809,1069", "821,1151"]
    position_delay = [10, 5, 5, 5, 8, 8, 5, 10]

    # 土遁去瓦当
    is_ok = ""
    try:
        is_ok = dao2_common.tu_dun_sui_mu(hwnd)
    except Exception as e:
        print(f"发生异常：{e}")
        is_ok = traceback.format_exc()

    if "" != is_ok:
        is_run_wa_da_huang = False
        messagebox.showwarning("警告", is_ok)
        return
    time.sleep(10)
    win_tool.press("w")
    time.sleep(1)

    while counter < max_count:
        if is_run_wa_da_huang is False:
            print("停止脚本")
            return

        if is_run_wa_da_huang is False:
            print("停止脚本")
            return

        if inx >= len(position):
            inx = 0

        # 导航
        on_xy = dao2_common.navigation_x_y(hwnd, position[inx])
        if isinstance(on_xy, str):
            messagebox.showwarning("警告", on_xy)
            return

        if is_run_wa_da_huang is False:
            print("停止脚本")
            return

        # 骑马
        dao2_common.qi_ma(hwnd)
        time.sleep(position_delay[inx])

        if is_run_wa_da_huang is False:
            print("停止脚本")
            return

        # 抬高相机
        dao2_common.camera_top(hwnd)
        inx += 1

        # 找大黄、挖大黄
        dh_count = 0
        while True:

            if is_run_wa_da_huang is False:
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

            win_tool.move_mouse(dh_xy[0], dh_xy[1])
            time.sleep(0.1)
            win_tool.move_left_click()
            time.sleep(6)
            counter += 1
            dh_count += 1

        if inx >= len(position):
            # 一轮完成 回到最早位置
            time.sleep(15)
    # sz_xy = dao2_common.find_lvse_shouzhang(hwnd)
    # if None is sz_xy:
    #     print("没有找到手掌")

    # 结束
    is_run_wa_da_huang = False
    messagebox.showwarning("通知", "挖大黄完成")


def wa_da_huang(hwnd):
    print(f"wa_da_huang={is_run_wa_da_huang}")
    t = threading.Thread(target=wa, args=(hwnd,))
    t.start()

