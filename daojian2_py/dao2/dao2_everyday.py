import win_tool
import threading
import time
import dao2_common
import traceback
from tkinter import messagebox
import bg_find_pic_area

w, h = win_tool.get_win_w_h()

is_run = False
lock = threading.Lock()


def jiu_feng_task(hwnd_array):
    t = threading.Thread(target=get_jiu_feng_task, args=(hwnd_array,), daemon=True)
    t.start()


# 接九凤任务
def get_jiu_feng_task(hwnd_array):
    global is_run

    if None is hwnd_array:
        messagebox.showwarning("警告", "未找到 刀剑2 窗口")
        is_run = False

    print(f"get_jiu_feng_task hwnd_array={hwnd_array}")
    # 土遁九凤
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        win_tool.activate_window(hwnd)
        time.sleep(0.3)
        try:
            is_ok = dao2_common.tu_dun_jiu_feng(hwnd)
        except Exception as e:
            print(f"发生异常：{e}")
            is_ok = traceback.format_exc()
            print(is_ok)

        if "" != is_ok:
            is_run = False
            messagebox.showwarning("警告", is_ok)
            return

    # 土遁后休息等逻辑同步
    time.sleep(9)

    # 刷一下逻辑同步
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        win_tool.activate_window(hwnd)
        time.sleep(0.3)
        win_tool.send_key("w", 3)

    time.sleep(1)

    position = ["250,857", "368,884"]

    # 导航去目标 252,854 悬赏牌
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        win_tool.activate_window(hwnd)
        time.sleep(0.3)
        # 导航
        on_xy = dao2_common.navigation_x_y(hwnd, position[0])
        if isinstance(on_xy, str):
            messagebox.showwarning("警告", on_xy)
            return

        # 骑马
        dao2_common.qi_ma(hwnd)

    # 休眠足够时间 去悬赏牌子
    time.sleep(41)

    # 轮流识图，找悬赏牌任务
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        win_tool.activate_window(hwnd)
        time.sleep(0.3)

        # 第一个任务
        msg = gain_jiu_feng_task(hwnd, "img/jiufeng_dangmo_get.bmp")
        if "" != msg:
            messagebox.showwarning("警告", msg)
            is_run = False
            return

        # 第二个任务
        msg = gain_jiu_feng_task(hwnd, "img/jiufeng_xiangmo_get.bmp")
        if "" != msg:
            messagebox.showwarning("警告", msg)
            is_run = False
            return

    # 接完任务，回台阶
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        win_tool.activate_window(hwnd)
        time.sleep(0.3)
        # 导航
        on_xy = dao2_common.navigation_x_y(hwnd, position[1])
        if isinstance(on_xy, str):
            messagebox.showwarning("警告", on_xy)
            is_run = False
            return
        # 按一次加速
        win_tool.send_key("ctrl", 1)

    # 到台阶上马
    time.sleep(41)
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        # 骑马
        dao2_common.qi_ma(hwnd)

    is_run = False
    messagebox.showwarning("通知", "接九凤完成")


def gain_jiu_feng_task(hwnd, img_name):
    # 抬高镜头
    dao2_common.camera_top(hwnd)

    xy = dao2_common.find_pic(hwnd, "img/jiufeng_xuanshangpai.bmp", 500, 100, int(w * 0.8), int(h * 0.5))
    if None is xy:
        print(f"{hwnd} 未找到悬赏牌 1")
        return "未找到 悬赏牌"

    # 点击悬赏牌
    win_tool.send_input_mouse_left_click(xy[0] + 20, xy[1] + 20)
    time.sleep(2)

    # 接任务
    xy = dao2_common.find_pic(hwnd, img_name, 400, int(h * 0.5), int(w * 0.7), h - 200)
    if None is xy:
        print(f"{hwnd} 未找到 {img_name}")
        return "未找到 荡魔九凤岭"

    # 接任务
    win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 5)
    time.sleep(1)

    # 交给我吧
    xy = dao2_common.find_pic(hwnd, "img/jiufeng_jiaogeiwoba.bmp", 200, 500, int(w * 0.6), int(h * 0.8))
    if None is xy:
        print(f"{hwnd} jiufeng_jiaogeiwoba 未找到")
        return "未找到 交给我吧"
    win_tool.send_input_mouse_left_click(xy[0] + 12, xy[1] + 10)
    time.sleep(1)
    return ""
