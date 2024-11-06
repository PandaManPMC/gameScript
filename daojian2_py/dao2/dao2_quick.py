import win_tool
import threading
import time
import dao2_common
import traceback
from tkinter import messagebox
import log3

w, h = win_tool.get_win_w_h()

lock = threading.Lock()

# 后台接通知、哨箭、任务分享、副本传送
is_run_receive_notify = False

# 后台一直按键
is_run_send_key_by_hwnd = False

# 草药研磨
is_run_cao_yao_yan_mo = False

# 自动组队
is_auto_team = False


# 开始研磨草药
def cao_yao_yan_mo(hwnd):
    log3.console(f"草药研磨 {hwnd}")
    c = 0
    start_time = time.time()
    global is_run_cao_yao_yan_mo

    # win_tool.activate_window(hwnd)
    # time.sleep(0.3)

    # 打开背包
    dao2_common.open_bag(hwnd)
    time.sleep(0.3)

    cao_yao = ["img/beibao_dahuang.bmp", "img/beibao_gancao.bmp"]

    while is_run_cao_yao_yan_mo:
        log3.console(f"研磨草药{c}个")
        win_tool.send_key_to_window(hwnd, "x")
        # 找草药
        xy = None
        for i in range(len(cao_yao)):
            xy = dao2_common.find_pic(hwnd, cao_yao[i], 200, 0, w - 200, int(h * 0.5), 0.8)
            if None is not xy:
                break
        if None is xy:
            is_run_cao_yao_yan_mo = False
            messagebox.showwarning("警告", "未找到 草药，请放在默认背包。")
            return
        # win_tool.send_input_mouse_left_click(xy[0] + 7, xy[1] + 7)
        win_tool.send_mouse_left_click(hwnd, xy[0] + 7, xy[1] + 7)
        time.sleep(0.3)

        # 确认窗口
        is_ok = False
        for i in range(3):
            xy = dao2_common.find_tu_dun_gou(hwnd)
            if None is xy:
                continue
            # win_tool.send_input_mouse_left_click(xy[0], xy[1])
            win_tool.send_mouse_left_click(hwnd, xy[0], xy[1])
            is_ok = True

        if not is_ok:
            # is_run_cao_yao_yan_mo = False
            # messagebox.showwarning("警告", "未找到 研磨 的确认窗口")
            # return
            log3.logger.info("未找到 研磨 的确认窗口")
            continue
        c += 1
        if c % 20 == 0:
            dao2_common.say_hwnd(hwnd, f"研磨草药{c}个 耗时{int(time.time() - start_time)}s")
        time.sleep(5.1)


# 一直按键，指定键和延迟
def send_key_by_hwnd(hwnd, key_to_send, delay):
    global is_run_send_key_by_hwnd
    key_code = win_tool.key_map.get(key_to_send)
    while is_run_send_key_by_hwnd:
        log3.console(f"hwnd={hwnd} 每 {float(delay)} 秒 发送 {key_code}")
        win_tool.send_key_to_window(hwnd, key_code)
        time.sleep(float(delay))


# 接通知
# 1.多窗口接任务共享
# 2.多窗口接穿云箭
# 3.多窗口进副本
def receive_notify(hwnd_array):
    t = threading.Thread(target=running_receive_notify, args=(hwnd_array,), daemon=True)
    t.start()


def running_receive_notify(hwnd_array):
    global is_run_receive_notify
    log3.console(f"start_receive_notify hwnd_array={hwnd_array}")

    if None is hwnd_array:
        messagebox.showwarning("警告", "未找到 刀剑2 窗口")
        is_run_receive_notify = False
        return

    # 不断循环，检测
    while is_run_receive_notify:
        time.sleep(0.25)
        for hwnd in hwnd_array:
            # 找 感叹号
            xy = dao2_common.find_pic(hwnd, "img/tongzhi_gantanhao.bmp", int(w * 0.35), int(h * 0.22), int(w*0.7), int(h * 0.9))
            if None is xy:
                log3.console(f"{hwnd} 未找到 tongzhi_gantanhao")
                continue

            win_tool.send_mouse_left_click(hwnd, xy[0] + 10, xy[1] + 10)
            time.sleep(0.05)

            # 找 勾
            for _ in range(10):
                xy = dao2_common.find_pic(hwnd, "img/sharerenwu_gou.bmp",  int(w * 0.3), int(h * 0.22), int(w*0.7), int(h * 0.7))
                if None is not xy:
                    # win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)
                    win_tool.send_mouse_left_click(hwnd, xy[0] + 10, xy[1] + 10)
                    time.sleep(0.02)
                    break

                xy = dao2_common.find_pic(hwnd, "img/chuangsong_tongyi.bmp", int(w * 0.3), int(h * 0.22), int(w*0.7), int(h * 0.7))
                if None is not xy:
                    # win_tool.send_input_mouse_left_click(xy[0] + 8, xy[1] + 7)
                    win_tool.send_mouse_left_click(hwnd, xy[0] + 10, xy[1] + 10)
                    time.sleep(0.02)
                    break

                # 重新找，因为切过去的时候，可能会发生改变
                xy = dao2_common.find_pic(hwnd, "img/tongzhi_gantanhao.bmp", int(w * 0.35), int(h * 0.22),
                                          int(w * 0.7), int(h * 0.9))
                if None is not xy:
                    # win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)
                    win_tool.send_mouse_left_click(hwnd, xy[0] + 10, xy[1] + 10)
                    time.sleep(0.1)


is_run_yi_jie_huan_qian = False


def yi_jie_huan_qian(hwnd):
    count = 0
    wallet_xy = None
    while is_run_yi_jie_huan_qian:
        xy = dao2_common.find_pic(hwnd, "img/yijie_qiandaizi.bmp", 0, int(h * 0.2), int(w * 0.4), int(h * 0.7), 0.8)
        if None is not xy:
            time.sleep(0.1)
            if None is wallet_xy:
                wallet_xy = xy
                dao2_common.say_hwnd(hwnd, f"检测到钱袋子 - {wallet_xy}")
            break
        time.sleep(0.2)

    q_d_xy = None
    # 鼠标不断点击
    while is_run_yi_jie_huan_qian:
        win_tool.send_mouse_right_click(hwnd, wallet_xy[0] + 7, wallet_xy[1] + 7)
        time.sleep(0.1)

        if None is q_d_xy:
            xy = dao2_common.find_pic(hwnd, "img/goumai_queding.bmp", int(w * 0.25), int(h * 0.25), int(w * 0.75), int(h * 0.75), 0.8)
            if None is not xy:
                q_d_xy = xy
                win_tool.send_mouse_left_click(hwnd, q_d_xy[0] + 8, q_d_xy[1] + 8)
                time.sleep(0.7)
                dao2_common.say_hwnd(hwnd, f"购买钱袋子 确定={q_d_xy}")
        else:
            win_tool.send_mouse_left_click(hwnd, q_d_xy[0] + 8, q_d_xy[1] + 8)
        time.sleep(0.1)
        count += 1
        if 0 != count and 0 == count % 300:
            dao2_common.say_hwnd(hwnd, f"{hwnd} 第 {count} 次 买钱袋子")


is_run_han_shui_huan_qian = False


def han_shui_huan_qian(hwnd):
    count = 0
    wallet_xy = None
    while is_run_han_shui_huan_qian:
        # 找打神鞭，然后往下偏移找钱袋子
        xy = dao2_common.find_pic(hwnd, "img/hanshui_dashenbian.bmp", 0, int(h * 0.2), int(w * 0.4), int(h * 0.7), 0.8)
        if None is not xy:
            time.sleep(0.1)
            if None is wallet_xy:
                wallet_xy = [xy[0] + 12, xy[1] + 90]
                dao2_common.say_hwnd(hwnd, f"检测到钱袋子 - {wallet_xy}")
            break
        time.sleep(0.2)

    q_d_xy = None
    # 鼠标不断点击
    while is_run_han_shui_huan_qian:
        win_tool.send_mouse_right_click(hwnd, wallet_xy[0] + 7, wallet_xy[1] + 7)
        time.sleep(0.1)

        if None is q_d_xy:
            xy = dao2_common.find_pic(hwnd, "img/goumai_queding.bmp", int(w * 0.25), int(h * 0.25), int(w * 0.75), int(h * 0.75), 0.8)
            if None is not xy:
                q_d_xy = xy
                win_tool.send_mouse_left_click(hwnd, q_d_xy[0] + 8, q_d_xy[1] + 8)
                time.sleep(0.7)
                dao2_common.say_hwnd(hwnd, f"购买钱袋子 确定={q_d_xy}")
        else:
            win_tool.send_mouse_left_click(hwnd, q_d_xy[0] + 8, q_d_xy[1] + 8)
        time.sleep(0.1)
        count += 1
        if 0 != count and 0 == count % 300:
            dao2_common.say_hwnd(hwnd, f"{hwnd} 第 {count} 次 买钱袋子")


is_run_gu_cha_huan_qian = False


def gu_cha_huan_qian(hwnd):
    count = 0
    wallet_xy = None
    while is_run_gu_cha_huan_qian:
        # 找通脉丸，然后往下偏移找钱袋子
        xy = dao2_common.find_pic(hwnd, "img/gucha_tongmaiwan.bmp", 0, int(h * 0.2), int(w * 0.4), int(h * 0.7), 0.8)
        if None is not xy:
            time.sleep(0.1)
            if None is wallet_xy:
                wallet_xy = [xy[0] + 12, xy[1] + 90]
                dao2_common.say_hwnd(hwnd, f"检测到钱袋子 - {wallet_xy}")
            break
        time.sleep(0.2)

    q_d_xy = None
    # 鼠标不断点击
    while is_run_gu_cha_huan_qian:
        win_tool.send_mouse_right_click(hwnd, wallet_xy[0] + 7, wallet_xy[1] + 7)
        time.sleep(0.1)

        if None is q_d_xy:
            xy = dao2_common.find_pic(hwnd, "img/goumai_queding.bmp", int(w * 0.25), int(h * 0.25), int(w * 0.75), int(h * 0.75), 0.8)
            if None is not xy:
                q_d_xy = xy
                win_tool.send_mouse_left_click(hwnd, q_d_xy[0] + 8, q_d_xy[1] + 8)
                time.sleep(0.7)
                dao2_common.say_hwnd(hwnd, f"购买钱袋子 确定={q_d_xy}")
        else:
            win_tool.send_mouse_left_click(hwnd, q_d_xy[0] + 8, q_d_xy[1] + 8)
        time.sleep(0.1)
        count += 1
        if 0 != count and 0 == count % 300:
            dao2_common.say_hwnd(hwnd, f"{hwnd} 第 {count} 次 买钱袋子")


# 自动组队
def auto_team(hwnd_array):
    t = threading.Thread(target=running_auto_team, args=(hwnd_array,), daemon=True)
    t.start()


def running_auto_team(hwnd_array):
    global is_auto_team
    log3.console(f"running_auto_team hwnd_array={hwnd_array}")

    if None is hwnd_array:
        messagebox.showwarning("警告", "未找到 刀剑2 窗口")
        is_run_receive_notify = False
        return

    # hwnds  = win_tool.get_all_window_handles_by_name("刀剑2")
    # log3.console(f"hwnds={hwnds}")

    # 不断循环，检测
    while is_auto_team:
        time.sleep(0.5)
        for hwnd in hwnd_array:
            xy = dao2_common.find_pic(hwnd, "img/tongzhi_zudui_jiahouyou.bmp", int(w * 0.35), int(h * 0.22), int(w*0.7), int(h * 0.9))
            if None is xy:
                log3.console(f"{hwnd} 未找到 tongzhi_zudui_jiahouyou")
                continue

            win_tool.send_mouse_left_click(hwnd, xy[0] + 10, xy[1] + 10)
            time.sleep(0.05)

            # 找 勾
            while True:
                # 重新找，因为切过去的时候，可能会发生改变
                xy = dao2_common.find_pic(hwnd, "img/tongzhi_zudui_jiahouyou.bmp", int(w * 0.35), int(h * 0.22),
                                          int(w * 0.7), int(h * 0.9))
                if None is not xy:
                    win_tool.send_mouse_left_click(hwnd, xy[0] + 10, xy[1] + 10)
                    time.sleep(0.05)

                xy = dao2_common.find_pic(hwnd, "img/sharerenwu_gou.bmp",  int(w * 0.3), int(h * 0.22), int(w*0.7), int(h * 0.7))
                if None is not xy:
                    # win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)
                    win_tool.send_mouse_left_click(hwnd, xy[0] + 10, xy[1] + 10)
                    time.sleep(0.02)
                    break


# 自动拾取：控制线程是否继续执行
runningCollect = False
lockCollect = threading.Lock()


def collect(window_name):
    key_to_send = 0x77  # 虚拟键码 'F8'
    while runningCollect:
        win_tool.send_key_to_all_windows(window_name, key_to_send)
        time.sleep(1)