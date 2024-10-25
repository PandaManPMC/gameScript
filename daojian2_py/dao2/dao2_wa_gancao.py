import time
import win_tool
import bg_find_pic_area
import threading
from tkinter import messagebox
import dao2_common
import traceback
import threading

w, h = win_tool.get_win_w_h()

is_run = False
lock = threading.Lock()

def gather(hwnd):
    print(f"gather_gan_cao gather={is_run}")
    t = threading.Thread(target=gather_gan_cao, args=(hwnd,), daemon=True)
    t.start()


def gather_gan_cao(hwnd):
    global is_run
    # 激活窗口
    win_tool.activate_window(hwnd)
    time.sleep(0.1)

    inx = 0
    max_count = 165
    counter = 0
    position = ["646,849", "642,940", "645,958", "688,1052", "790,1057"]
    position_delay = [10, 5, 4, 11, 7]

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
            time.sleep(22)

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

            win_tool.move_mouse(dh_xy[0], dh_xy[1])
            time.sleep(0.2)
            win_tool.mouse_left_click()
            time.sleep(6)
            counter += 1
            dh_count += 1

        if inx >= len(position):
            # 一轮完成 回到最早位置
            is_finish = True

    # 结束
    is_run_wa_da_huang = False
    messagebox.showwarning("通知", "挖甘草完成")
