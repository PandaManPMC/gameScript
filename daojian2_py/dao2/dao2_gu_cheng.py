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

# 拾取次数 不能是单数
COLLECT_MAX_COUNT = 22

# 存储数量
storage_count = 0

# 死亡次数
die_count = 0


# 复活
def resurgence(hwnd):
    global die_count
    xy = dao2_common.is_die(hwnd)
    if None is xy:
        return None
    die_count += 1
    # dao2_common.say(f"存储次数={storage_count},死亡次数={die_count}", hwnd)
    dao2_common.say_hwnd(hwnd, f"凶手 画个圈圈诅咒你 0.0 死亡次数={die_count}")
    time.sleep(0.5)
    # win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
    win_tool.send_mouse_left_click(hwnd, xy[0] + 5, xy[1] + 5)
    time.sleep(7)

    for _ in range(3):
        # 是否到黄泉
        xy = dao2_common.find_pic(hwnd, "img/yiditu.bmp", int(w * 0.7), int(h * 0.5), w, h)
        if None is xy:
            time.sleep(3)
        else:
            break

    # 复活延迟，逻辑同步
    win_tool.send_key_to_window_frequency(hwnd, "w", 3)
    time.sleep(3)
    win_tool.send_key_to_window_frequency(hwnd, "w", 3)
    time.sleep(3)
    return xy


# 捡卷并存储
def collect_storage(hwnd):
    global is_run
    global storage_count

    position = ["975,629", "1105,632", "1081,659", "1083,695",
                # 贪狼区域
                "1140,719", "1122,767", "1063,751",
                # 开始回走
                "1063,712", "1058,661", "1026,645", "1022,729", "976,698", "1010,636",
                "948,655", "972,764",
                # 中断区域
                "903,762", "864,724", "854,784", "817,725",
                "746,723", "817,782", "859,818", "886,876", "892,805",
                "1000,805",
                # 天台附近
                "1011,896",
                # 围着天台下
                "1019,964", "1061,981", "1061,1071", "989,1072", "991,975",
                # 上天台
                "1008,1045", "1037,1021",
                # 下天台
                "1031,937", "1079,908", "1083,1088", "962,1091",
                # 去北部
                "942,1381", "1112,1391", "1104,1400", "1121,1305", "1090,1367",
                # 去东
                "1198,1221", "1299,1185", "1396,1108", "1402,917", "1251,868",
                # 隐蔽的角落
                "1301,724", "1169,721", "1267,797", "1204,849",
                # 向西部进发
                "1151,962", "984,845", "1003,951", "885,937", "818,937",
                # 西部一圈回去
                "747,811", "756,955", "718,907", "654,907", "655,1106",
                # 回中
                "746,1110", "693,1046", "786,1074", "929,1062",
                # 回南
                "959,1077", "958,947",
                "1065,868", "1023,749", "909,795",
                "891,757", "932,724"]
    delay = [1, 4, 1, 2,
             # 贪狼区域
             2, 1, 4,
             # 开始回走
             2, 2, 1, 2, 2, 2,
             1, 3,
             # 中断区域
             2, 1, 1, 1,
             2, 2, 2, 2, 1,
             2,
             # 天台附近
             1,
             # 围着天台下
             2, 2, 3, 3, 3,
             # 上天台
             2, 1,
             # 下天台
             2, 3, 4, 3,
             # 去北部
             10, 6, 2, 3, 2,
             # 去东
             9, 4, 5, 4, 5,
             # 隐蔽的角落
             5, 5, 5, 5,
             # 向西部进发
             4, 8, 3, 4, 5,
             # 西部一圈回去
             5, 5, 2, 2, 8,
             # 回中
             3, 2, 6, 8,
             # 回南
             1, 3,
             3, 3, 3,
             1, 2]
    collect_count = 0

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
        # messagebox.showwarning("警告", nn)
        # is_run = False
        return "未找到帮会使者"

    # 骑马
    dao2_common.qi_ma(hwnd)
    time.sleep(12)

    if None is not resurgence(hwnd):
        return "is_resurgence"

    if is_run is False:
        log3.console("停止脚本")
        return

    # 帮会使者 因为逻辑延迟可能到不了
    for k in range(10):

        if not is_run:
            log3.console("停止脚本")
            return

        if None is not resurgence(hwnd):
            return "is_resurgence"

        xy = dao2_common.find_pic(hwnd, "img/jingrugucheng.bmp", int(w * 0.2), int(h * 0.4), int(w * 0.8), h - 10)
        if None is xy:
            log3.logger.info("未找到 jingrugucheng.bmp！")
            time.sleep(3)
            continue

        # win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)
        win_tool.send_mouse_left_click(hwnd, xy[0] + 10, xy[1] + 10)
        time.sleep(6.5)
        if is_run is False:
            log3.console("停止脚本")
            return

        # 是否在古城了
        xy = dao2_common.find_pic(hwnd, "img/yiditu.bmp", int(w * 0.7), int(h*0.5), w, h)
        if None is xy and k == 8:
            log3.logger.info("img/yiditu.bmp 不在古城")
            messagebox.showwarning("警告", "未找到 yiditu.bmp！ 不在古城")
            is_run = False
            return "不在古城，逻辑错误"
        elif None is xy:
            continue
        else:
            # 已在古城 打断循环
            break

    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 进行一次异地图判断,不是,就土遁重走
    yi_di_tu_xy = dao2_common.find_pic(hwnd, "img/yiditu.bmp", int(w * 0.7), int(h*0.5), w, h)
    if None is yi_di_tu_xy:
        dao2_common.esc_and_back(hwnd)
        time.sleep(0.25)
        dao2_common.close_bag(hwnd)
        return "restart"

    # 循环走点，边走边捡，死亡检测（死亡黄泉瓦当重来）
    while is_run:
        inx = 0
        is_over = False
        while inx < len(position):
            # 关闭 6 点的弹窗
            dao2_common.close_6_oclock_dialog(hwnd)

            if None is not resurgence(hwnd):
                return "is_resurgence"

            if is_run is False:
                log3.console("停止脚本")
                return
            on_xy = dao2_common.navigation_x_y(hwnd, position[inx])
            if isinstance(on_xy, str):
                messagebox.showwarning("警告", on_xy)
                is_run = False
                return
            dao2_common.qi_ma(hwnd)

            # 不断拾取,每 delay 1 拾取 n 次
            print(f"坐标{position[inx]} - 延迟{delay[inx]}")
            for j in range(delay[inx] * 14):
                if is_run is False:
                    log3.console("停止脚本")
                    return
                win_tool.send_key_to_window(hwnd, "f8")
                time.sleep(0.07)

            inx += 1
            # 是否在拾取
            is_collect = False
            round_collect_count = 0
            while True:
                if is_run is False:
                    log3.console("停止脚本")
                    return
                for _ in range(3):
                    win_tool.send_key_to_window(hwnd, "f8")
                    time.sleep(0.03)
                time.sleep(1.5)

                dao2_common.camera_forward(hwnd)

                xy = dao2_common.find_pic(hwnd, "img/shiqujindu.bmp", int(w * 0.3), int(h * 0.3), int(w * 0.7), h-100, 0.8)
                if None is xy:
                    log3.console("没在拾取")
                    break
                else:
                    log3.console(f"正在拾取{collect_count}")

                    # 在拾取，休眠  拾取。继续拾取
                    time.sleep(15.1)
                    is_collect = True
                    collect_count += 1
                    round_collect_count += 1
                    if COLLECT_MAX_COUNT <= collect_count:
                        is_over = True
                        break
            if COLLECT_MAX_COUNT <= collect_count:
                is_over = True
                break
            # 发生过拾取
            if is_collect:
                inx -= 1
                # 如果拾取超过 COLLECT_MAX_COUNT 的一半，则回去存储
                if round_collect_count > COLLECT_MAX_COUNT / 2:
                    is_over = True
                    log3.logger.info(f"在一点捡超过一半，回去存储")
                    break
        if COLLECT_MAX_COUNT <= collect_count or is_over:
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

    # 检查战斗状态
    while True:
        is_battle = dao2_common.is_battle(hwnd)
        if not is_battle:
            break
        dao2_common.navigation_x_y(hwnd, "858,729")
        time.sleep(2)

    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 去瓦当
    try:
        is_ok = dao2_common.tu_dun_wa_dang(hwnd)
    except Exception as e:
        log3.console(f"发生异常：{e}")
        is_ok = traceback.format_exc()
        log3.console(is_ok)

    if "" != is_ok:

        if None is not resurgence(hwnd):
            return "is_resurgence"

        is_run = False
        messagebox.showwarning("警告", is_ok)
        return
    time.sleep(7)
    # win_tool.send_key("w", 3)
    win_tool.send_key_to_window_frequency(hwnd, "w", 3)
    time.sleep(3)
    if is_run is False:
        log3.console("停止脚本")
        return
    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 存仓库
    # 去仓库
    while is_run:
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

        res = to_storage2(hwnd)
        if "not_find_qianzhuang" != res:
            return res


def to_storage2(hwnd):
    global is_run
    global storage_count

    # 关闭 6 点的弹窗
    dao2_common.close_6_oclock_dialog(hwnd)

    if None is not resurgence(hwnd):
        return "is_resurgence"

    open_qian_zhuang = False
    for _ in range(7):
        xy = dao2_common.find_pic(hwnd, "img/cangku_qianzhuang.bmp", int(w * 0.2), int(h * 0.5), int(w*0.75), h-100)
        if None is xy:
            log3.console("没找到 cangku_qianzhuang")
            time.sleep(3)
            continue
        # win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
        win_tool.send_mouse_left_click(hwnd, xy[0] + 5, xy[1] + 5)
        time.sleep(1)
        open_qian_zhuang = True
        break

    if None is not resurgence(hwnd):
        return "is_resurgence"

    if not open_qian_zhuang:
        log3.logger.error(f"古城捡卷 有人捣乱 去仓库路上被阻挡")
        return to_storage(hwnd)

    # 存钱庄
    storage(hwnd, 1)
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

        # messagebox.showwarning("警告", nn)
        # is_run = False
        log3.logger.error(f" 古城捡卷 {hwnd} {nn}")
        return

    time.sleep(1)
    xy = dao2_common.find_pic(hwnd, "img/cangku_linlangge.bmp", int(w * 0.2), int(h * 0.5), int(w*0.75), h-100)
    if None is xy:
        log3.console("没找到 cangku_linlangge")
        log3.logger.info("没找到 cangku_linlangge")
        return
    # win_tool.send_input_mouse_left_click(xy[0]+5, xy[1]+5)
    win_tool.send_mouse_left_click(hwnd, xy[0]+5, xy[1]+5)
    time.sleep(1)
    storage(hwnd, 2)
    time.sleep(0.3)
    storage_count += 1


def storage(hwnd, num):
    global is_run
    global storage_count

    # 找到背包的位置
    xy = dao2_common.find_pic(hwnd, "img/dakai_debeibao.bmp", int(w * 0.1), 0, w-200, int(h * 0.5), 0.8)
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
        for j in range(8):
            # # 关闭 6 点的弹窗
            # dao2_common.close_6_oclock_dialog(hwnd)

            if is_run is False:
                log3.console("停止脚本")
                return
            b_x = f_x + o_x * j
            b_y = f_y + o_y * i
            # win_tool.send_input_mouse_right_click(b_x, b_y)
            win_tool.send_mouse_right_click(hwnd, b_x, b_y)
            time.sleep(0.25)
            # 确定按钮,多存
            xy = dao2_common.find_pic(hwnd, "img/cangku_queding.bmp", 400, 100, w-400, int(h * 0.6), 0.8)
            if None is xy:
                log3.console("没找到 cangku_queding")
                continue
            # win_tool.send_input_mouse_left_click(xy[0], xy[1])
            win_tool.send_mouse_left_click(hwnd, xy[0], xy[1])
            time.sleep(0.1)

    # 存壮骨
    if 1 == num:
        xy = dao2_common.find_pic(hwnd, "img/beibao_zhuangguwang.bmp", int(w * 0.2), int(h * 0.1), w, int(h * 0.9), 0.9)
        if None is not xy:
            # win_tool.send_input_mouse_right_click(xy[0]+5, xy[1]+5)
            win_tool.send_mouse_right_click(hwnd, xy[0]+5, xy[1]+5)
            time.sleep(0.25)
            xy = dao2_common.find_pic(hwnd, "img/cangku_queding.bmp", 400, 100, w - 400, int(h * 0.6))
            if None is not xy:
                # win_tool.send_input_mouse_left_click(xy[0], xy[1])
                win_tool.send_mouse_left_click(hwnd, xy[0], xy[1])
                time.sleep(0.1)
        else:
            log3.console("没有壮骨丸")


def try_collect(hwnd):
    while is_run:
        try:
            if None is not resurgence(hwnd):
                dao2_common.say(f"检测到死亡", hwnd)
            collect(hwnd)
        except Exception as e:
            log3.logger.warn(f"发生异常：{e} {traceback.format_exc()}")
            dao2_common.say(f"检测到异常={e}, 重新启动中", hwnd)
            gc.collect()
            time.sleep(15)


def collect(hwnd):
    global is_run
    # win_tool.activate_window(hwnd)
    # time.sleep(0.3)

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
    time.sleep(7)
    # win_tool.send_key("w", 3)
    win_tool.send_key_to_window_frequency(hwnd, "w", 3)
    time.sleep(3)
    if is_run is False:
        log3.console("停止脚本")
        return

    while is_run:
        time.sleep(0.2)

        # 去帮会使者 进入古城
        res = collect_storage(hwnd)
        log3.logger.info(f"collect_storage = {res}")

        if "restart" == res:
            log3.logger.error(f"{hwnd} 好像有人捣乱,无法进入古城,重新跑")

        if "未找到帮会使者" == res:
            dao2_common.esc_and_back(hwnd)

        if "is_resurgence" == res:
            # 到复活点了
            log3.console("已到复活点")
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
            # win_tool.send_key("w", 3)
            win_tool.send_key_to_window_frequency(hwnd, "w", 3)
            time.sleep(2)
            if is_run is False:
                log3.console("停止脚本")
                return
        else:
            # dao2_common.say(f"存储次数={storage_count},死亡次数={die_count}", hwnd)
            dao2_common.say_hwnd(hwnd, f"存储次数={storage_count},死亡次数={die_count}")
        log3.console(f"storage_count={storage_count}")


def gu_cheng_collect(hwnd):
    global is_run
    with lock:
        # 开启子线程
        t = threading.Thread(target=try_collect, args=(hwnd,), daemon=True)
        t.start()
