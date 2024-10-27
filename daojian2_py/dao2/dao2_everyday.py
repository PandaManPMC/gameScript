import win_tool
import threading
import time
import dao2_common
import traceback
from tkinter import messagebox

w, h = win_tool.get_win_w_h()

is_run = False
lock = threading.Lock()


# 琼云跳舞
def start_qion_yun_dance(hwnd_array):
    global is_run
    with lock:
        is_run = not is_run
        if is_run:
            t = threading.Thread(target=qion_yun_dance, args=(hwnd_array,), daemon=True)
            t.start()


def qion_yun_dance(hwnd_array):
    global is_run
    for hwnd in hwnd_array:
        win_tool.activate_window(hwnd)
        time.sleep(0.3)
        try:
            is_ok = dao2_common.tu_dun_qion_yun(hwnd)
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

    position = ["958,677"]
    delay = [25]

    # 导航去目标
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        win_tool.activate_window(hwnd)
        time.sleep(0.3)

        dao2_common.close_bag(hwnd)

        # 导航
        on_xy = dao2_common.navigation_x_y(hwnd, position[0])
        if isinstance(on_xy, str):
            messagebox.showwarning("警告", on_xy)
            return

        # 骑马
        dao2_common.qi_ma(hwnd)

    # 休眠足够时间
    time.sleep(delay[0])
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        win_tool.activate_window(hwnd)
        time.sleep(0.3)

        # 找露无霜
        xy = None
        for j in range(5):
            # 相机抬摆正
            dao2_common.camera_forward()

            xy = dao2_common.find_pic(hwnd, "img/qiongyun_luwushuang.bmp", 500, 100, w - 500, int(h * 0.9))
            if None is xy:
                print(f"{hwnd} 未找到 qiongyun_luwushuang")
                time.sleep(0.3)
                if is_run is False:
                    print("停止脚本")
                    return
                continue

        if None is xy:
            messagebox.showwarning("警告", "未找到露无霜")
            is_run = False
            return

        while True:
            win_tool.send_input_mouse_right_click(xy[0] + 12, xy[1] + 50)
            time.sleep(0.3)
            if is_run is False:
                print("停止脚本")
                return
            # 找露无霜 头像
            xy2 = dao2_common.find_pic(hwnd, "img/qiongyun_luwushuang_touxiang.bmp", 500, 0, w - 500, int(h * 0.3))
            if None is xy2:
                print(f"{hwnd} 未找到 qiongyun_luwushuang_touxiang")
                time.sleep(0.2)
                if is_run is False:
                    print("停止脚本")
                    return
                continue
            break

        # 找到露无霜，打开背包，找舞天令
        dao2_common.open_bag(hwnd)
        time.sleep(0.2)

        # 找舞天令
        xy = dao2_common.find_pic(hwnd, "img/beibao_wutianling.bmp", 0, 0, w, int(h * 0.5), 0.8)
        if None is xy:
            print(f"{hwnd} 未找到 beibao_wutianling")
            messagebox.showwarning("警告", "背包中没有舞天令")
            is_run = False
            return

        win_tool.send_input_mouse_right_click(xy[0] + 6, xy[1] + 6)
        continue

    is_run = False
    dao2_common.say("脚本完成，开始跳舞")
    messagebox.showwarning("通知", "脚本完成，开始跳舞")


def niao_shan_task(hwnd_array):
    t = threading.Thread(target=get_niao_shan_task, args=(hwnd_array,), daemon=True)
    t.start()


def get_niao_shan_task(hwnd_array):
    global is_run
    print(f"get_niao_shan_task hwnd_array={hwnd_array}")

    if None is hwnd_array:
        messagebox.showwarning("警告", "未找到 刀剑2 窗口")
        is_run = False

    # 土遁鸟山
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        win_tool.activate_window(hwnd)
        time.sleep(0.3)
        try:
            is_ok = dao2_common.tu_dun_niao_shan(hwnd)
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

    position = ["529,237"]
    delay = [20]

    # 导航去目标
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

    # 休眠足够时间
    time.sleep(delay[0])

    # 轮流识图
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        win_tool.activate_window(hwnd)
        time.sleep(0.3)

        # 杨青
        get_niao_shan_task_hero(hwnd, "img/niaoshan_yangqing.bmp", "img/niaoshan_baozhuyuanhun.bmp")

        if is_run is False:
            print("停止脚本")
            return

        # 慕非焉
        get_niao_shan_task_hero(hwnd, "img/niaoshan_mufeiyan.bmp", "img/niaoshan_zhoumosishi.bmp")
        get_niao_shan_task_hero(hwnd, "img/niaoshan_mufeiyan.bmp", "img/niaoshan_yidaorumo.bmp")
        get_niao_shan_task_hero(hwnd, "img/niaoshan_mufeiyan.bmp", "img/niaoshan_mohuajinjiao.bmp")
        get_niao_shan_task_hero(hwnd, "img/niaoshan_mufeiyan.bmp", "img/niaoshan_moshanyishou.bmp")

        if is_run is False:
            print("停止脚本")
            return

        # 葛喻成
        get_niao_shan_task_hero(hwnd, "img/niaoshan_geyucheng.bmp", "img/niaoshan_gongshan.bmp")

        # 接完任务，去台阶等 540，265
        on_xy = dao2_common.navigation_x_y(hwnd, "540,265")
        if isinstance(on_xy, str):
            messagebox.showwarning("警告", on_xy)
            is_run = False
            return
        dao2_common.say(f"接完鸟山任务={hwnd}")

    is_run = False
    messagebox.showwarning("通知", "接鸟山完成")


def get_niao_shan_task_hero(hwnd, img_name_hero, img_name_task):
    while True:
        if is_run is False:
            print("停止脚本")
            return

        # 抬高镜头
        dao2_common.camera_top()

        xy = dao2_common.find_pic(hwnd, img_name_hero, 500, 100, int(w * 0.8), int(h * 0.6))
        if None is xy:
            print(f"{hwnd} 未找到 {img_name_hero}")
            time.sleep(0.5)

            continue

        # 鼠标点击 hero
        win_tool.send_input_mouse_left_click(xy[0]+5, xy[1]-15)
        time.sleep(1.5)
        xy = dao2_common.find_pic(hwnd, img_name_task, 500, 200, w - 400, int(h * 0.9))
        if None is xy:
            print(f"{hwnd} 未找到 {img_name_task}")
            # messagebox.showwarning("警告", f"{hwnd} 未找到 {img_name_task}")
            time.sleep(0.3)
            # if is_run is False:
            #     print("停止脚本")
            #     return
            # 重新找英雄
            continue
        win_tool.send_input_mouse_left_click(xy[0]+5, xy[1] + 5)
        time.sleep(0.3)
        xy = dao2_common.find_pic(hwnd, "img/jiufeng_jiaogeiwoba.bmp", 0, 100, w - 500, int(h * 0.9))
        if None is xy:
            print(f"{hwnd} 未找到 jiufeng_jiaogeiwoba")
            messagebox.showwarning("警告", f"{hwnd} 未找到 jiufeng_jiaogeiwoba")
            time.sleep(0.3)
            if is_run is False:
                print("停止脚本")
                return
        # 交给我吧
        win_tool.send_input_mouse_left_click(xy[0]+2, xy[1]+5)
        time.sleep(0.5)
        break


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

    # 休眠足够时间 去悬赏牌子，前5s 检测死亡
    time.sleep(8)
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        if None is not dao2_common.is_die(hwnd):
            print("已死亡，停止脚本1")
            is_run = False
            return
        win_tool.activate_window(hwnd)
        time.sleep(0.3)
        win_tool.send_key("ctrl", 1)
    time.sleep(32)

    # 轮流识图，找悬赏牌任务
    for hwnd in hwnd_array:
        if is_run is False:
            print("停止脚本")
            return
        win_tool.activate_window(hwnd)
        time.sleep(0.3)

        if None is not dao2_common.is_die(hwnd):
            print("已死亡，停止脚本2")
            is_run = False
            return

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
        win_tool.activate_window(hwnd)
        time.sleep(0.3)

        # 骑马
        dao2_common.qi_ma(hwnd)
        dao2_common.say(f"接完九凤任务={hwnd}")

    is_run = False
    messagebox.showwarning("通知", "接九凤完成")


def gain_jiu_feng_task(hwnd, img_name):
    # 抬高镜头
    dao2_common.camera_top()

    xy = dao2_common.find_pic(hwnd, "img/jiufeng_xuanshangpai2.bmp", 500, 50, int(w * 0.8), int(h * 0.5))
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
    xy = dao2_common.find_pic(hwnd, "img/jiufeng_jiaogeiwoba.bmp", 100, 500, int(w * 0.6), int(h * 0.8))
    if None is xy:
        print(f"{hwnd} jiufeng_jiaogeiwoba 未找到")
        return "未找到 交给我吧"
    win_tool.send_input_mouse_left_click(xy[0] + 12, xy[1] + 10)
    time.sleep(1)
    return ""
