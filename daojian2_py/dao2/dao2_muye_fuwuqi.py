import win_tool
import threading
import time
import dao2_common
import traceback
from tkinter import messagebox

w, h = win_tool.get_win_w_h()

is_run = False
lock = threading.Lock()

# 死亡次数
die_count = 0


def start_mu_ye(hwnd, delay):
    print("start_mu_ye")
    t = threading.Thread(target=go_mu_ye, args=(hwnd, delay, ), daemon=True)
    t.start()


def go_mu_ye(hwnd, delay):
    print(f"my_ye hwnd={hwnd} delay={delay}")
    win_tool.activate_window(hwnd)
    time.sleep(0.3)

    while True:
        if "is_resurgence" == exercise(hwnd, delay):
            time.sleep(5)
        else:
            time.sleep(2)


def exercise(hwnd, delay):

    position = ["1112,1023", "1025,1075"]
    position_delay = [22, 8]

    for inx in range(len(position)):
        # 导航
        on_xy = dao2_common.navigation_x_y(hwnd, position[inx])
        if isinstance(on_xy, str):
            messagebox.showwarning("警告", on_xy)
            return

        # 骑马
        dao2_common.qi_ma(hwnd)
        # 休眠足够时间
        time.sleep(position_delay[inx])

        if None is not resurgence(hwnd):
            return "is_resurgence"

    # 找稻草人
    while True:
        win_tool.send_key("tab")
        time.sleep(0.2)
        if None is not resurgence(hwnd):
            return "is_resurgence"

        xy2 = dao2_common.find_pic(hwnd, "img/muye_daocaoren.bmp", 300, 0, w - 20, int(h * 0.3))
        if None is xy2:
            time.sleep(0.3)
            continue
        # 找到稻草人，打断
        break

    exe_count = 0
    # 攻击稻草人
    while True:
        win_tool.send_key("1")
        time.sleep(float(delay))
        if None is not resurgence(hwnd):
            return "is_resurgence"
        exe_count += 1

        # 每练习 10 次，就打开背包检测一下需不需要炼魂
        if exe_count % 10 == 0:
            xy2 = dao2_common.find_pic(hwnd, "img/zhuangbei.bmp", 300, 0, w - 20, int(h * 0.5))
            if None is xy2:
                # 按 B 打开背包
                win_tool.send_key("b")
                time.sleep(0.3)
            # 检测 副武器所在位置

        # 通过找到 八卦，在偏移 X
        xy = dao2_common.find_pic(hwnd, "img/zhuangbei_guaxiang.bmp", 0, 400, w - 200, int(h * 0.8))
        if None is xy:
            continue

        # 偏移 X ，找成长等级
        for i in range(5):
            print("1")
            # 找 成长等级 20 级
            # 找 成长等级 40 级
            # 找 成长等级 60 级

        # 关闭背包
        win_tool.send_key("b")


        # 已经要炼魂，去找副武器大师
        # 副武器大师 964,698


# 复活
def resurgence(hwnd):
    global die_count
    xy = dao2_common.is_die_dian(hwnd)
    if None is xy:
        return None
    die_count += 1
    dao2_common.say(f"死亡次数={die_count}")

    time.sleep(1)
    win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
    time.sleep(1)
    return xy




