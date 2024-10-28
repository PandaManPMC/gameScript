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

# 死亡次数
die_count = 0

# 副武器映射
zhuan_bei = {"img/zhuangbei_shuangjiegun.bmp": "img/beibao_shuangjiegun.bmp",
             "img/zhuangbei_yushan.bmp": "img/beibao_yushan.bmp"}

# 是否炼魂的 flag
lian_hun_flag = ""


def start_mu_ye(hwnd, delay):
    print("start_mu_ye")
    t = threading.Thread(target=go_mu_ye, args=(hwnd, delay, ), daemon=True)
    t.start()


def go_mu_ye(hwnd, delay):
    global is_run

    log3.console(f"my_ye hwnd={hwnd} delay={delay}")
    win_tool.activate_window(hwnd)
    time.sleep(0.3)
    zb = check_fuwuqi_name(hwnd)
    log3.console(f"找到的装备= {zb}, lian_hun_flag={lian_hun_flag}")
    dao2_common.say(f"找到的装备= {zb}, lian_hun_flag={lian_hun_flag}")
    if "" == zb:
        is_run = False
        messagebox.showwarning("警告", f"装备 未找到 副武器{zb}")
        return
    while True:
        if "is_resurgence" == exercise(hwnd, delay, zb):
            time.sleep(5)
        else:
            time.sleep(2)
        if None is not resurgence(hwnd):
            return "is_resurgence"


# 获得副武器的名字与炼魂标志
# 自动炼魂的关键
# 在脚本开始之初，得到一个脚本等级
# 在练副武器每10次，就检查一次脚本等级，当与第一次获取不同时，就去炼魂，炼魂完成后，再把新获取的更新上去。
def check_fuwuqi_name(hwnd):
    global is_run
    global lian_hun_flag

    dao2_common.open_zhuangbei(hwnd)
    time.sleep(0.3)

    for key in zhuan_bei:
        log3.console(f"键: {key}")
        xy = dao2_common.find_pic(hwnd, key, 0, 400, w - 300, int(h * 0.8))
        if None is xy:
            time.sleep(0.1)
            continue
        # 移动鼠标到装备上
        win_tool.move_mouse(xy[0] + 8, xy[1] + 8)
        time.sleep(0.3)
        # 找 成长等级 20 级
        xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_20.bmp", 50, 0, w - 20, int(h * 0.4), 0.8)
        if xy is not None:
            lian_hun_flag = "成长等级：20"
            return key

        # 找 成长等级 40 级
        xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_40.bmp", 50, 0, w - 20, int(h * 0.4))
        if xy is not None:
            lian_hun_flag = "成长等级：40"
            return key

        # 找 成长等级 60 级
        xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_60.bmp", 50, 0, w - 20, int(h * 0.4))
        if xy is not None:
            lian_hun_flag = "成长等级：60"
            return key

        return key
    return ""


def get_lian_hun_new_flag(hwnd, zb):
    global is_run
    global lian_hun_flag
    dao2_common.open_zhuangbei(hwnd)
    time.sleep(0.3)

    xy = dao2_common.find_pic(hwnd, zb, 0, 400, w - 300, int(h * 0.8))
    if None is xy:
        # is_run = False
        # messagebox.showwarning("警告", f"装备 未找到 副武器{zb}")
        return lian_hun_flag

    # 移动鼠标到装备上
    win_tool.move_mouse(xy[0] + 8, xy[1] + 8)
    time.sleep(0.3)

    # 找 成长等级 20 级
    # 找 成长等级 40 级
    xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_20.bmp", 50, 0, w - 20, int(h * 0.4), 0.8)
    if xy is not None:
        return "成长等级：20"

    xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_40.bmp", 50, 0, w - 20, int(h * 0.4))
    if xy is not None:
        return "成长等级：40"

    # 找 成长等级 60 级
    xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_60.bmp", 50, 0, w - 20, int(h * 0.4))
    if xy is not None:
        return "成长等级：60"


def wear(hwnd, zb):
    global is_run
    log3.console("检查装备 wear")
    # 检查装备
    dao2_common.open_zhuangbei(hwnd)
    time.sleep(0.3)
    xy = dao2_common.find_pic(hwnd, zb, 0, 400, w - 200, int(h * 0.8))
    if None is xy:
        time.sleep(0.3)

        # 打开背包，安装装备
        dao2_common.open_bag(hwnd)
        time.sleep(0.3)

        # 在背包找副武器,装备
        xy = dao2_common.find_pic(hwnd, zhuan_bei[zb], 200, 0, w - 200, int(h * 0.5))
        if None is xy:
            is_run = False
            time.sleep(0.3)
            messagebox.showwarning("警告", f"背包 未找到 副武器{zb}")
            return
        win_tool.send_input_mouse_right_click(xy[0] + 5, xy[1] + 5)
        time.sleep(0.3)
        # 关闭背包
        dao2_common.close_bag(hwnd)
        # 关闭装备
        dao2_common.close_zhuangbei(hwnd)
        time.sleep(0.3)
    else:
        log3.console(f"装备{zb}已经安装")


def lian_hun(hwnd, zb, new_flag):
    global is_run
    # 已经要炼魂，去找副武器大师
    # 副武器大师 964,698
    # 关闭 6 点的弹窗
    dao2_common.close_6_oclock_dialog(hwnd)

    # 导航
    on_xy = dao2_common.navigation_x_y(hwnd, "1108,989")
    if isinstance(on_xy, str):
        messagebox.showwarning("警告", on_xy)
        is_run = False
        return
    time.sleep(9)
    # 骑马
    dao2_common.qi_ma(hwnd)
    time.sleep(6)

    if None is not resurgence(hwnd):
        return "is_resurgence"

    on_xy = dao2_common.navigation_x_y(hwnd, "964,698")
    if isinstance(on_xy, str):
        messagebox.showwarning("警告", on_xy)
        is_run = False
        return

    # 休眠足够时间
    time.sleep(20)

    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 打开装备
    dao2_common.open_zhuangbei(hwnd)
    time.sleep(0.2)

    # 找装备
    xy = dao2_common.find_pic(hwnd, zb, 0, 400, w - 200, int(h * 0.8))
    if None is xy:
        is_run = False
        time.sleep(0.3)
        messagebox.showwarning("警告", f"未找到 {zb}")
        return

    win_tool.send_input_mouse_right_click(xy[0] + 8, xy[1] + 8)
    time.sleep(0.1)
    dao2_common.close_zhuangbei(hwnd)
    time.sleep(0.1)

    # 镜头
    dao2_common.camera_top()

    while is_run:
        if None is not resurgence(hwnd):
            return "is_resurgence"

        # 找副武器大师
        xy = dao2_common.find_pic(hwnd, "img/fuwuqidashi_log.bmp", 200, 0, w - 200, int(h * 0.5))
        if None is xy:
            time.sleep(0.3)
            continue

        win_tool.send_input_mouse_right_click(xy[0] + 10, xy[1] + 10)
        time.sleep(0.3)

        # 找副武器大师头像
        xy_tx = dao2_common.find_pic(hwnd, "img/fuwuqidashi_tx.bmp", 200, 0, w - 200, int(h * 0.4))
        if None is xy_tx:
            time.sleep(0.3)
            continue

        win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)
        time.sleep(0.3)
        break

    # 选择炼魂
    xy = dao2_common.find_pic(hwnd, "img/fuwuqi_lianhun.bmp", 300, 500, w - 300, h - 100)
    if None is xy:
        is_run = False
        time.sleep(0.3)
        messagebox.showwarning("警告", "未找到 炼魂 选项")
        return

    win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
    time.sleep(0.3)

    # 在背包找副武器,放进炼魂
    xy = dao2_common.find_pic(hwnd, zhuan_bei[zb], 200, 0, w - 200, int(h * 0.5))
    if None is xy:
        is_run = False
        time.sleep(0.3)
        messagebox.showwarning("警告", f"未找到 副武器{zb}")
        return
    win_tool.send_input_mouse_right_click(xy[0] + 5, xy[1] + 5)
    time.sleep(0.3)

    # 点击炼魂
    xy = dao2_common.find_pic(hwnd, "img/fuwuqi_lianhun_btn.bmp", 100, 500, w - 200, int(h * 0.5))
    if None is xy:
        is_run = False
        time.sleep(0.3)
        messagebox.showwarning("警告", "未找到 炼魂按钮")
        return
    win_tool.send_input_mouse_left_click(xy[0] + 2, xy[1] + 3)

    # 更新炼魂 flag
    lian_hun_flag = new_flag

    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 炼魂完成
    dao2_common.say(f"{zb} 炼魂完成")


def exercise(hwnd, delay, zb):
    global is_run
    global lian_hun_flag

    position = ["1112,1023", "1025,1075"]
    position_delay = [22, 8]

    for inx in range(len(position)):
        if not is_run:
            return
        # 导航
        on_xy = dao2_common.navigation_x_y(hwnd, position[inx])
        if isinstance(on_xy, str):
            messagebox.showwarning("警告", on_xy)
            return

        # 骑马
        dao2_common.qi_ma(hwnd)
        # 休眠足够时间
        time.sleep(position_delay[inx])

        if 0 == inx:
            wear(hwnd, zb)

        if None is not resurgence(hwnd):
            return "is_resurgence"

    # 找稻草人
    while is_run:
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

    new_flag = ""
    exe_count = 0
    # 攻击稻草人
    while is_run:

        # 进行检测，防止打死稻草人或者被人捣乱推出擂台
        if exe_count % 11 == 0:
            # 关闭 6 点的弹窗
            dao2_common.close_6_oclock_dialog(hwnd)

            xy2 = dao2_common.find_pic(hwnd, "img/muye_daocaoren.bmp", 300, 0, w - 20, int(h * 0.3))
            if None is xy2:
                win_tool.send_key("tab")
                time.sleep(0.3)
                # 如果还是没有稻草人，重新跑
                xy3 = dao2_common.find_pic(hwnd, "img/muye_daocaoren.bmp", 300, 0, w - 20, int(h * 0.3))
                if None is xy3:
                    return "not find daocaoren"

        win_tool.send_key("1")
        time.sleep(float(delay))
        if None is not resurgence(hwnd):
            return "is_resurgence"
        exe_count += 1

        # 每练习 10 次，就打开装备检测一下需不需要炼魂
        if exe_count % 10 == 0:
            # 找成长等级
            new_flag = get_lian_hun_new_flag(hwnd, zb)
            if lian_hun_flag == new_flag:
                log3.console(f"不需要炼魂 lian_hun_flag={lian_hun_flag}")
                continue
            else:
                # 打断循环，去炼魂
                break

    # 已经要炼魂
    return lian_hun(hwnd, zb, new_flag)


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




