import win_tool
import threading
import time
import dao2_common
import traceback
from tkinter import messagebox

w, h = win_tool.get_win_w_h()

lock = threading.Lock()

# 后台接通知、哨箭、任务分享、副本传送
is_run_receive_notify = False

# 后台一直按键
is_run_send_key_by_hwnd = False

# 草药研磨
is_run_cao_yao_yan_mo = False


# 开始研磨草药
def cao_yao_yan_mo(hwnd):
    print(f"草药研磨 {hwnd}")
    c = 0
    start_time = time.time()
    global is_run_cao_yao_yan_mo
    win_tool.activate_window(hwnd)
    time.sleep(0.3)
    key_code = win_tool.key_map.get("x")

    # 打开背包
    dao2_common.open_bag(hwnd)

    cao_yao = ["img/beibao_dahuang.bmp", "img/beibao_gancao.bmp"]

    while is_run_cao_yao_yan_mo:
        print(f"研磨草药{c}个")
        win_tool.send_key_to_window(hwnd, key_code)
        # 找草药
        xy = None
        for i in range(len(cao_yao)):
            xy = dao2_common.find_pic(hwnd, cao_yao[i], 200, 0, w - 200, int(h * 0.5))
            if None is not xy:
                break
        if None is xy:
            is_run_cao_yao_yan_mo = False
            messagebox.showwarning("警告", "未找到 草药")
            return
        win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
        time.sleep(0.3)

        # 确认窗口
        is_ok = False
        for i in range(3):
            xy = dao2_common.find_tu_dun_gou(hwnd)
            if None is xy:
                continue
            win_tool.send_input_mouse_left_click(xy[0], xy[1])
            is_ok = True

        if not is_ok:
            is_run_cao_yao_yan_mo = False
            messagebox.showwarning("警告", "未找到 研磨 的确认窗口")
            return
        c += 1
        if c % 20 == 0:
            dao2_common.say(f"研磨草药{c}个 耗时{time.time() - start_time}s")
        time.sleep(5.1)


# 一直按键，指定键和延迟
def send_key_by_hwnd(hwnd, key_to_send, delay):
    global is_run_send_key_by_hwnd
    key_code = win_tool.key_map.get(key_to_send)
    while is_run_send_key_by_hwnd:
        print(f"hwnd={hwnd} 每 {float(delay)} 秒 发送 {key_code}")
        win_tool.send_key_to_window(hwnd, key_code)
        time.sleep(float(delay))


# 接通知
# 1.多窗口接任务共享
# 2.多窗口接穿云箭
# 3.多窗口进副本
# 4.自动组队
def receive_notify(hwnd_array):
    t = threading.Thread(target=running_receive_notify, args=(hwnd_array,), daemon=True)
    t.start()


def running_receive_notify(hwnd_array):
    global is_run_receive_notify
    print(f"start_receive_notify hwnd_array={hwnd_array}")

    if None is hwnd_array:
        messagebox.showwarning("警告", "未找到 刀剑2 窗口")
        is_run_receive_notify = False
        return

    hwnds  = win_tool.get_all_window_handles_by_name("刀剑2")
    print(f"hwnds={hwnds}")

    # 不断循环，检测
    while is_run_receive_notify:

        if is_run_receive_notify is False:
            print("脚本停止")
            return
        is_re = False
        for hwnd in hwnd_array:
            # 找 感叹号
            xy = dao2_common.find_pic(hwnd, "img/tongzhi_gantanhao.bmp", 400, 300, w - 500, int(h * 0.8))
            if None is xy:
                print(f"{hwnd} 未找到 tongzhi_gantanhao")
                time.sleep(0.05)
                continue

            # 找到，激活窗口，点击
            win_tool.activate_window(hwnd)
            time.sleep(0.08)

            # 找 勾
            while True:
                # 重新找，因为切过去的时候，可能会发生改变
                xy = dao2_common.find_pic(hwnd, "img/tongzhi_gantanhao.bmp", 400, 300, w - 500, int(h * 0.8))
                win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)

                is_re = True
                time.sleep(0.1)

                xy = dao2_common.find_pic(hwnd, "img/sharerenwu_gou.bmp", 400, 400, w - 500, int(h * 0.7), 0.8)
                if None is not xy:
                    win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)
                    time.sleep(0.02)
                    break

                xy = dao2_common.find_pic(hwnd, "img/chuangsong_tongyi.bmp", 400, 400, w - 500, int(h * 0.7))
                if None is not xy:
                    win_tool.send_input_mouse_left_click(xy[0] + 8, xy[1] + 7)
                    time.sleep(0.02)
                    break

        if 0 != len(hwnds):
            if is_re:
                win_tool.activate_window(hwnds[0])

