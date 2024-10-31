import gc

import win_tool
import threading
import time
import dao2_common
import traceback
from tkinter import messagebox
import log3

w, h = win_tool.get_win_w_h()

is_run = False
lock = threading.Lock()

# 挖宝按 V，打哈桑技能 E，开宝箱技能 R

# 次数
COLLECT_MAX_COUNT = 13

# 存储数量
storage_count = 0

# 死亡次数
die_count = 0

# 挖宝总数
TREASURE_COUNT = 3


# 复活
def resurgence(hwnd):
    global die_count
    xy = dao2_common.is_die(hwnd)
    if None is xy:
        return None
    die_count += 1
    dao2_common.say(f"resurgence 存储次数={storage_count},死亡次数={die_count}")

    time.sleep(1)
    win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
    time.sleep(1)
    return xy


# 捡卷并存储
def collect_storage(hwnd, position_inx):
    global is_run
    global storage_count

    # 路线
    position_arr = [
        ["953,626", "987,627", "1035,630"],
        ["940,739", "901,765", "867,769"],
        ["927,690", "908,722", "857,721"],]
    collect_count = 0
    position = position_arr[position_inx]

    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 去帮会使者
    # on_xy = dao2_common.navigation_x_y(hwnd, "677,514")
    # if isinstance(on_xy, str):
    #     messagebox.showwarning("警告", on_xy)
    #     is_run = False
    #     return

    # 关闭 6 点的弹窗
    dao2_common.close_6_oclock_dialog(hwnd)

    # 导航去找帮会使者
    nn = dao2_common.navigation_name(hwnd, "img/daohang_banghuishizhe.bmp")
    if isinstance(nn, str):
        messagebox.showwarning("警告", nn)
        is_run = False
        return

    # 骑马
    dao2_common.qi_ma(hwnd)
    time.sleep(12)

    if None is not resurgence(hwnd):
        return "is_resurgence"

    if is_run is False:
        log3.console("停止脚本")
        return

    # 抬高镜头
    # dao2_common.camera_top()

    # 帮会使者可能被挡住，这里循环等待
    while True:
        if is_run is False:
            log3.console("停止脚本")
            return

        if None is not resurgence(hwnd):
            return "is_resurgence"

        xy = dao2_common.find_pic(hwnd, "img/jingrugucheng.bmp", int(w * 0.2), int(h * 0.4), int(w * 0.8), h - 50)
        if None is xy:
            is_run = False
            log3.console("未找到 jingrugucheng.bmp！")
            time.sleep(1.5)
            # messagebox.showwarning("警告", "未找到 jingrugucheng.bmp！")
            # return
            continue

        win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)
        time.sleep(6)
        if is_run is False:
            log3.console("停止脚本")
            return

        # 是否在古城了
        xy = dao2_common.find_pic(hwnd, "img/yiditu.bmp", 1000, 600, w, h)
        if None is xy:
            log3.console("不在古城")
            messagebox.showwarning("警告", "未找到 yiditu.bmp！ 不在古城")
            is_run = False
            return
        else:
            # 已在古城 打断循环
            break

    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 循环走点，死亡检测（死亡黄泉瓦当重来）
    for i in range(len(position)):
        # 关闭 6 点的弹窗
        dao2_common.close_6_oclock_dialog(hwnd)

        if None is not resurgence(hwnd):
            return "is_resurgence"

        if is_run is False:
            log3.console("停止脚本")
            return
        on_xy = dao2_common.navigation_x_y(hwnd, position[i])
        if isinstance(on_xy, str):
            messagebox.showwarning("警告", on_xy)
            is_run = False
            return
        # dao2_common.qi_ma(hwnd)

        time.sleep(4)
        # 按 V 挖宝
        win_tool.send_key("v", 1)
        time.sleep(0.2)
        win_tool.send_key("w", 1)
        time.sleep(1)
        dao2_common.camera_top()
        # 第一次挖 打断，逻辑同步，第二次挖才是真的挖
        win_tool.send_key("v", 1)

        time.sleep(12)
        # 按 Tab
        win_tool.send_key("tab", 1)
        time.sleep(0.3)

        # 如果出现哈桑头像，就闪避然后按 E。
        xy2 = dao2_common.find_pic(hwnd, "img/gucheng_hasang.bmp", 300, 0, w - 50, int(h * 0.3))
        if None is not xy2:
            dao2_common.say("出现哈桑 - 攻击哈桑")
            win_tool.send_key("w", 3)
            time.sleep(0.6)
            win_tool.send_key("E", 1)
            time.sleep(3)
        else:
            for k in range(3):
                xy2 = dao2_common.find_pic(hwnd, "img/gucheng_baoxiang.bmp", 300, 0, w - 50, int(h * 0.3))
                if None is not xy2:
                    # 不是哈桑，按 R 打宝箱
                    win_tool.send_key_to_window_frequency(hwnd, "R")
                    time.sleep(1)
                    break
                # 按 Tab
                win_tool.send_key_to_window_frequency(hwnd, "tab")
                time.sleep(0.2)

        treasure_count = 0
        # 是否在拾取
        while True:
            if is_run is False:
                log3.console("停止脚本")
                return

            if 0 != treasure_count and treasure_count % 5 == 0:
                if None is not resurgence(hwnd):
                    return "is_resurgence"

            if 15 <= treasure_count:
                break

            key_to_send = 0x77  # 虚拟键码 'F8'
            win_tool.send_key_to_window(hwnd, key_to_send)
            if 14 == treasure_count:
                time.sleep(1.6)
            else:
                time.sleep(1.2)

            dao2_common.camera_forward()

            xy = dao2_common.find_pic(hwnd, "img/shiqujindu.bmp", int(w * 0.3), int(h * 0.4), int(w * 0.8), h - 200, 0.8)
            if None is xy:
                log3.console("没在拾取")
                treasure_count += 1
                continue
            else:
                log3.console(f"正在拾取{collect_count}")
                # 在拾取，休眠 15s 拾取。继续拾取
                time.sleep(15.5)
                collect_count += 1
                if COLLECT_MAX_COUNT <= collect_count:
                    break
        if COLLECT_MAX_COUNT <= collect_count:
            break

    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 捡够数量，回瓦当
    if is_run is False:
        log3.console("停止脚本")
        return

    log3.console(f"捡够数量，回瓦当 collect_count={collect_count}")
    return to_storage(hwnd)


def to_storage(hwnd):
    global is_run
    global storage_count

    # 关闭 6 点的弹窗
    dao2_common.close_6_oclock_dialog(hwnd)

    # 去瓦当
    try:
        is_ok = dao2_common.tu_dun_wa_dang(hwnd)
    except Exception as e:
        log3.console(f"发生异常：{e}")
        is_ok = traceback.format_exc()
        log3.console(is_ok)

    if "" != is_ok:
        is_run = False
        messagebox.showwarning("警告", is_ok)
        return
    time.sleep(8)
    win_tool.send_key("w", 3)
    time.sleep(2)
    if is_run is False:
        log3.console("停止脚本")
        return
    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 存仓库

    # 打开导航
    on_xy = dao2_common.open_navigation(hwnd)
    if isinstance(on_xy, str):
        messagebox.showwarning("警告", on_xy)
        is_run = False
        return
    # 鼠标移动到导航的上面，可以操作鼠标滚轮
    win_tool.move_mouse(on_xy[0] - 50, on_xy[1] - 200)
    time.sleep(0.1)

    # 去仓库
    nn = dao2_common.navigation_name(hwnd, "img/daohang_wodecangku.bmp")
    if isinstance(nn, str):
        log3.logger.error(f"treasure 未找到 img/daohang_wodecangku.bmp")
        if None is not resurgence(hwnd):
            return "is_resurgence"

        # messagebox.showwarning("警告", nn)
        # is_run = False
        return to_storage(hwnd)
    # 骑马
    dao2_common.qi_ma(hwnd)
    time.sleep(16)

    # 关闭 6 点的弹窗
    dao2_common.close_6_oclock_dialog(hwnd)

    if None is not resurgence(hwnd):
        return "is_resurgence"

    xy = dao2_common.find_pic(hwnd, "img/cangku_qianzhuang.bmp", 300, 600, int(w * 0.7), h - 100)
    if None is xy:
        log3.console("没找到 cangku_qianzhuang")
        return
    time.sleep(0.1)
    win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
    time.sleep(1)
    # 存钱庄
    storage(hwnd)
    # 存琳琅阁
    time.sleep(0.3)
    if is_run is False:
        log3.console("停止脚本")
        return

    # 去仓库
    nn = dao2_common.navigation_name(hwnd, "img/daohang_wodecangku.bmp")
    if isinstance(nn, str):
        if None is not resurgence(hwnd):
            return "is_resurgence"

        messagebox.showwarning("警告", nn)
        is_run = False
        return

    time.sleep(1)
    xy = dao2_common.find_pic(hwnd, "img/cangku_linlangge.bmp", int(w * 0.2), int(h * 0.5), int(w*0.75), h-100)
    if None is xy:
        log3.console("没找到 cangku_linlangge")
        log3.logger.info("没找到 cangku_linlangge")
        return
    time.sleep(0.1)
    win_tool.send_input_mouse_left_click(xy[0]+5, xy[1]+5)
    time.sleep(0.6)
    storage(hwnd)
    time.sleep(0.3)
    storage_count += 1


def storage(hwnd):
    global is_run
    global storage_count

    # 找到背包的位置
    xy = dao2_common.find_pic(hwnd, "img/dakai_debeibao.bmp", int(w * 0.2), 0, w - 200, int(h * 0.5), 0.8)
    if None is xy:
        log3.console("没找到 dakai_debeibao")
        return
    # 背包位置作为基位置，对1080p 的处理，处理出第一个背包点位，以及偏移量

    # 2k 下的第一个点
    f_x = xy[0] + 27
    f_y = xy[1] + 64
    # 偏移
    o_x = 46
    o_y = 46
    if 1920 == w:
        # 1080p 处理
        f_x = xy[0] + int(27 * 0.75)
        f_y = xy[1] + int(64 * 0.75)
        o_x = 47 * 0.75
        o_y = 47 * 0.75

    # 轮询背包 8 * 4 格子
    for i in range(4):
        # 关闭 6 点的弹窗
        # dao2_common.close_6_oclock_dialog(hwnd)
        for j in range(8):

            if is_run is False:
                log3.console("停止脚本")
                return
            b_x = f_x + o_x * j
            b_y = f_y + o_y * i

            # 先移动到上面，等一会查看是不是凝神宝袋
            win_tool.move_mouse(b_x, b_y)
            time.sleep(0.2)
            xy_bd = dao2_common.find_pic(hwnd, "img/beibao_ningshenbaodai.bmp", int(w * 0.1), 0, w - 20, int(h * 0.5), 0.8)
            if None is not xy_bd:
                # 点击凝神宝袋
                win_tool.send_input_mouse_left_click(b_x, b_y)
                time.sleep(0.1)
                # 移动到背包外面
                win_tool.move_mouse(f_x - 120, f_y + 100)
                time.sleep(0.1)
                # 点击左键 删除
                win_tool.mouse_left_click()
                time.sleep(0.2)
                # 确定删除凝神宝袋
                xy = dao2_common.find_pic(hwnd, "img/beibao_shanchuqueding.bmp", int(w * 0.2), int(h * 0.1), int(w * 0.7), int(h * 0.7), 0.8)
                if None is not xy:
                    win_tool.send_input_mouse_left_click(xy[0], xy[1] + 7)
                    time.sleep(0.1)
                continue

            # 存其它
            win_tool.send_input_mouse_right_click(b_x, b_y)
            time.sleep(0.15)

            # 确定按钮,多存
            xy = dao2_common.find_pic(hwnd, "img/cangku_queding.bmp", int(w * 0.2), int(h * 0.1), int(w * 0.7), int(h * 0.7), 0.8)
            if None is xy:
                log3.console("没找到 cangku_queding")
                continue
            win_tool.send_input_mouse_left_click(xy[0], xy[1])
            time.sleep(0.1)

    # 存壮骨
    xy = dao2_common.find_pic(hwnd, "img/beibao_zhuangguwang.bmp", int(w * 0.3), int(h * 0.2), w, int(h * 0.9), 0.9)
    if None is not xy:
        win_tool.send_input_mouse_right_click(xy[0] + 5, xy[1] + 5)
        time.sleep(0.2)
        xy = dao2_common.find_pic(hwnd, "img/cangku_queding.bmp", int(w * 0.2), int(h * 0.1), int(w * 0.7), int(h * 0.7), 0.8)
        if None is not xy:
            win_tool.send_input_mouse_left_click(xy[0], xy[1])
            time.sleep(0.1)
    else:
        log3.console("没有壮骨丸")


def try_collect(hwnd):
    while is_run:
        try:
            if None is not resurgence(hwnd):
                dao2_common.say(f"检测到死亡")
            collect(hwnd)
        except Exception as e:
            log3.console(f"发生异常：{e} {traceback.format_exc()}")
            dao2_common.say(f"检测到异常={e}, 重新启动中")
            gc.collect()
            time.sleep(15)


def collect(hwnd):
    global is_run
    win_tool.activate_window(hwnd)
    time.sleep(0.3)

    # 路线
    position_inx = 0

    # 去瓦当
    try:
        is_ok = dao2_common.tu_dun_wa_dang(hwnd)
    except Exception as e:
        log3.console(f"发生异常：{e}")
        is_ok = traceback.format_exc()
        log3.console(is_ok)

    if "" != is_ok:
        is_run = False
        messagebox.showwarning("警告", is_ok)
        return
    time.sleep(8)
    win_tool.send_key("w", 3)
    time.sleep(2)
    if is_run is False:
        log3.console("停止脚本")
        return

    while is_run:
        # 关闭 6 点的弹窗
        dao2_common.close_6_oclock_dialog(hwnd)
        # 去帮会使者 进入古城
        res = collect_storage(hwnd, position_inx)
        position_inx += 1
        if "is_resurgence" == res:
            # 到复活点了
            log3.console("已到复活点")
            time.sleep(10)
            try:
                # 关闭 6 点的弹窗
                dao2_common.close_6_oclock_dialog(hwnd)
                is_ok = dao2_common.tu_dun_wa_dang(hwnd)
            except Exception as e:
                log3.console(f"发生异常：{e}")
                is_ok = traceback.format_exc()
                log3.console(is_ok)

            if "" != is_ok:
                is_run = False
                messagebox.showwarning("警告", is_ok)
                return
            time.sleep(8)
            win_tool.send_key("w", 3)
            time.sleep(2)
            if is_run is False:
                log3.console("停止脚本")
                return
        log3.console(f"storage_count={storage_count}")
        dao2_common.say(f"存储次数={storage_count},死亡次数={die_count}")


def gu_cheng_treasure(hwnd):
    global is_run
    with lock:
        # 开启子线程
        t = threading.Thread(target=try_collect, args=(hwnd,), daemon=True)
        t.start()
