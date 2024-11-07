import win_tool
import threading
import time
import dao2_common
import traceback
from tkinter import messagebox
import log3
import ocr_tool

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

# 成长等级
cheng_zhang_level = ""


def start_mu_ye(hwnd, delay):
    print("start_mu_ye")
    t = threading.Thread(target=go_mu_ye, args=(hwnd, delay, ), daemon=True)
    t.start()


def go_mu_ye(hwnd, delay):
    global is_run

    log3.console(f"my_ye hwnd={hwnd} delay={delay}")
    # win_tool.activate_window(hwnd)
    # time.sleep(0.3)
    zb = check_fuwuqi_name(hwnd)
    dao2_common.say_hwnd(hwnd, f"找到的装备= {zb}, lian_hun_flag={lian_hun_flag}")

    if "" == zb:
        is_run = False
        messagebox.showwarning("警告", f"装备 未找到 副武器{zb}")
        return

    while is_run:
        try:
            if "is_resurgence" == exercise(hwnd, delay, zb):
                time.sleep(5)
            else:
                time.sleep(2)
            if None is not resurgence(hwnd):
                log3.logger.info("is_resurgence")
                time.sleep(5)
        except Exception as e:
            log3.logger.error(f"{e} {traceback.format_exc()}")
            time.sleep(5)


# 获得副武器的名字与炼魂标志
# 自动炼魂的关键
# 在脚本开始之初，得到一个脚本等级
# 在练副武器每10次，就检查一次脚本等级，当与第一次获取不同时，就去炼魂，炼魂完成后，再把新获取的更新上去。
def check_fuwuqi_name(hwnd):
    global is_run
    global lian_hun_flag
    global cheng_zhang_level

    dao2_common.open_zhuangbei(hwnd)
    time.sleep(0.3)

    for key in zhuan_bei:
        log3.console(f"键: {key}")
        xy = dao2_common.find_pic(hwnd, key, 0, 400, w - 300, int(h * 0.8))
        if None is xy:
            time.sleep(0.1)
            continue
        # 移动鼠标到装备上
        # win_tool.move_mouse(xy[0] + 8, xy[1] + 8)
        win_tool.send_mouse_middle_click(hwnd, xy[0] + 8, xy[1] + 8)
        time.sleep(0.3)
        lian_hun_flag = ocr_tool.capture_window_to_str(hwnd, int(w * 0.2), 0, int(w * 0.75), int(h * 0.7), "成长等级")
        cheng_zhang_level = lian_hun_flag
        log3.logger.info(f"key={key} cheng_zhang_level={cheng_zhang_level}")
        time.sleep(0.2)
        for i in range(99):
            xy = dao2_common.find_pic(hwnd, "img/zhuangbei_closeall.bmp", int(w * 0.2), int(h * 0.4), int(w * 0.8),
                                      int(h * 0.95))
            if None is not xy:
                if 10 >= i:
                    win_tool.send_key_to_window_frequency(hwnd, "esc", 1)
                    time.sleep(0.3)
                    continue
                win_tool.send_mouse_left_click(hwnd, xy[0] + 5, xy[0] + 8)
                time.sleep(0.3)
            else:
                break

        # # 找 成长等级 20 级
        # xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_20.bmp", 50, 0, w - 20, int(h * 0.4), 0.9)
        # if xy is not None:
        #     lian_hun_flag = "成长等级：20"
        #     return key
        #
        # # 找 成长等级 40 级
        # xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_40.bmp", 50, 0, w - 20, int(h * 0.4), 0.9)
        # if xy is not None:
        #     lian_hun_flag = "成长等级：40"
        #     return key

        # 找 成长等级 60 级
        # xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_60.bmp", 50, 0, w - 20, int(h * 0.4), 0.81)
        # if xy is not None:
        #     lian_hun_flag = "成长等级：60"
        #     return key

        return key
    return ""


def get_lian_hun_new_flag(hwnd, zb):
    global is_run
    global lian_hun_flag
    global cheng_zhang_level
    dao2_common.open_zhuangbei(hwnd)
    time.sleep(0.3)

    xy = dao2_common.find_pic(hwnd, zb, 0, 400, w - 300, int(h * 0.8))
    if None is xy:
        # is_run = False
        # messagebox.showwarning("警告", f"装备 未找到 副武器{zb}")
        return lian_hun_flag

    # 移动鼠标到装备上
    # win_tool.move_mouse(xy[0] + 8, xy[1] + 8)
    win_tool.send_mouse_middle_click(hwnd, xy[0] + 8, xy[1] + 8)
    time.sleep(0.3)

    le = ocr_tool.capture_window_to_str(hwnd, int(w * 0.2), 0, int(w * 0.75), int(h * 0.7), "成长等级")
    if "" != le:
        cheng_zhang_level = le

    time.sleep(0.2)
    for i in range(99):
        xy = dao2_common.find_pic(hwnd, "img/zhuangbei_closeall.bmp", int(w * 0.2), int(h * 0.4), int(w * 0.8), int(h * 0.95))
        if None is not xy:
            if 10 >= i:
                win_tool.send_key_to_window_frequency(hwnd, "esc", 1)
                time.sleep(0.3)
                continue
            win_tool.send_mouse_left_click(hwnd, xy[0] + 5, xy[0] + 8)
            time.sleep(0.3)
        else:
            break

    # 找 成长等级 20 级
    # xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_20.bmp", 50, 0, w - 20, int(h * 0.4), 0.85)
    # if xy is not None:
    #     return "成长等级：20"

    # 找 成长等级 40 级
    # xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_40.bmp", 50, 0, w - 20, int(h * 0.4), 0.85)
    # if xy is not None:
    #     return "成长等级：40"

    # 找 成长等级 60 级
    # xy = dao2_common.find_pic(hwnd, "img/fuwuqi_chengzhangdengji_60.bmp", 50, 0, w - 20, int(h * 0.4), 0.8)
    # if xy is not None:
    #     return "成长等级：60"

    return cheng_zhang_level


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
        # win_tool.send_input_mouse_right_click(xy[0] + 5, xy[1] + 5)
        win_tool.send_mouse_right_click(hwnd, xy[0] + 5, xy[1] + 5)
        time.sleep(0.3)
        # 关闭背包
        dao2_common.close_bag(hwnd)
        # 关闭装备
        dao2_common.close_zhuangbei(hwnd)
        time.sleep(0.3)
    else:
        log3.logger.info(f"装备{zb}已经安装")


def find_fu_wu_qi_da_shi(hwnd):
    # 镜头
    dao2_common.camera_top(hwnd)
    # 记录顶层 hwnd，完成炼魂操作后，还要切回去
    top_hwnd = win_tool.GetForegroundWindow()

    for i in range(10):
        time.sleep(1)

        if None is not resurgence(hwnd):
            return "is_resurgence"

        # 找副武器大师
        xy = dao2_common.find_pic(hwnd, "img/fuwuqidashi_log.bmp", int(w * 0.1), int(h * 0.1), int(w * 0.9), int(h * 0.6))
        if None is xy:
            time.sleep(0.3)
            continue

        # 激活窗口，完成炼魂
        win_tool.activate_window(hwnd)
        time.sleep(0.3)

        # win_tool.send_input_mouse_right_click(xy[0] + 10, xy[1] + 10)
        win_tool.send_mouse_right_click(hwnd, xy[0] + 10, xy[1] + 10)
        time.sleep(0.3)

        # 找副武器大师头像
        xy_tx = dao2_common.find_pic(hwnd, "img/fuwuqidashi_tx.bmp", int(w * 0.2), 0, int(w * 0.8), int(h * 0.4))
        if None is xy_tx:
            time.sleep(0.3)
            continue

        # win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)
        win_tool.send_mouse_left_click(hwnd, xy[0] + 10, xy[1] + 10)
        time.sleep(0.3)

        time.sleep(0.1)
        win_tool.move_mouse(xy[0] + 10, xy[1] + 10)
        time.sleep(0.1)
        win_tool.activate_window(top_hwnd)
        win_tool.move_mouse(0, h)
        time.sleep(0.1)
        return True
    return False


def xiu_li(hwnd):
    global is_run
    # 找到炼魂选项，往下拉
    xy = dao2_common.find_pic(hwnd, "img/fuwuqi_lianhun.bmp", int(w*0.1), int(h * 0.5), int(w * 0.8), h - 100)
    if None is xy:
        is_run = False
        time.sleep(0.3)
        messagebox.showwarning("警告", "未找到 炼魂 选项")
        return

    # win_tool.move_mouse(xy[0]+11, xy[1]+11)
    # time.sleep(0.2)
    # win_tool.scroll_mouse_down(240)
    # time.sleep(0.3)
    win_tool.scroll_mouse_wheel_at(hwnd, xy[0]+11, xy[1]+11, -240)
    time.sleep(0.3)

    # 打开副武器兑换
    xy = dao2_common.find_pic(hwnd, "img/fuwuqi_duihuanji.bmp", int(w * 0.1), int(h * 0.5), int(w * 0.8), h - 100)
    if None is xy:
        log3.logger.error("xiu_li 未找到 fuwuqi_duihuanji")
        return
    # win_tool.send_input_mouse_left_click(xy[0] + 10, xy[1] + 10)
    win_tool.send_mouse_left_click(hwnd, xy[0] + 10, xy[1] + 10)
    time.sleep(0.3)

    # 修理装备
    xy = dao2_common.find_pic(hwnd, "img/zhuangbeixiuli.bmp", 0, int(h * 0.2), int(w * 0.5), h - 100, 0.8)
    if None is xy:
        log3.logger.error("xiu_li 未找到 zhuangbeixiuli")
        return
    # win_tool.send_input_mouse_left_click(xy[0] + 12, xy[1] + 12)
    win_tool.send_mouse_left_click(hwnd, xy[0] + 12, xy[1] + 12)
    time.sleep(0.3)
    win_tool.move_mouse_to(hwnd, xy[0] + 300, xy[1] + 300)

    # 按两次 esc，关闭商店和背包
    win_tool.send_key_to_window_frequency(hwnd, "esc", 1)
    time.sleep(0.1)
    win_tool.send_key_to_window_frequency(hwnd, "esc", 1)
    time.sleep(0.1)


def lian_hun(hwnd, zb, new_flag):
    global is_run
    global lian_hun_flag

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

    on_xy = dao2_common.navigation_x_y(hwnd, "1109,870")
    if isinstance(on_xy, str):
        messagebox.showwarning("警告", on_xy)
        is_run = False
        return
    # 骑马
    time.sleep(7)

    if None is not resurgence(hwnd):
        return "is_resurgence"

    on_xy = dao2_common.navigation_x_y(hwnd, "964,698")
    if isinstance(on_xy, str):
        messagebox.showwarning("警告", on_xy)
        is_run = False
        return

    # 休眠足够时间
    time.sleep(17)

    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 打开副武器大师
    if not find_fu_wu_qi_da_shi(hwnd):
        # 没找到副武器大师，很可能是路上有人捣乱，递归重新找
        return lian_hun(hwnd, zb, new_flag)

    # 修理装备
    xiu_li(hwnd)
    time.sleep(0.2)

    # 打开装备
    dao2_common.open_zhuangbei(hwnd)
    time.sleep(0.3)

    # 找装备
    xy = dao2_common.find_pic(hwnd, zb, 0, 400, w - 200, int(h * 0.8))
    if None is xy:
        is_run = False
        time.sleep(0.3)
        messagebox.showwarning("警告", f"未找到 {zb}")
        return
    # 卸下装备
    # win_tool.send_input_mouse_right_click(xy[0] + 11, xy[1] + 11)
    win_tool.send_mouse_right_click(hwnd, xy[0] + 11, xy[1] + 11)
    time.sleep(0.3)
    dao2_common.close_zhuangbei(hwnd)
    time.sleep(0.3)

    # 副武器大师
    find_fu_wu_qi_da_shi(hwnd)

    # 选择炼魂
    xy = dao2_common.find_pic(hwnd, "img/fuwuqi_lianhun.bmp", 200, int(h * 0.5), int(w * 0.8), h - 100)
    if None is xy:
        is_run = False
        time.sleep(0.3)
        messagebox.showwarning("警告", "未找到 炼魂 选项")
        return

    # win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
    win_tool.send_mouse_left_click(hwnd, xy[0] + 5, xy[1] + 5)
    time.sleep(0.35)

    # 在背包找副武器,放进炼魂
    xy = dao2_common.find_pic(hwnd, zhuan_bei[zb], int(w * 0.2), 0, w - 100, int(h * 0.5))
    if None is xy:
        is_run = False
        time.sleep(0.3)
        messagebox.showwarning("警告", f"未找到 副武器{zb}")
        return
    # win_tool.send_input_mouse_right_click(xy[0] + 7, xy[1] + 7)
    win_tool.send_mouse_right_click(hwnd, xy[0] + 7, xy[1] + 7)
    time.sleep(0.3)

    # 点击炼魂
    xy = dao2_common.find_pic(hwnd, "img/fuwuqi_lianhun_btn.bmp", 50, int(h * 0.3), int(w * 0.7), int(h * 0.9))
    if None is xy:
        is_run = False
        time.sleep(0.3)
        messagebox.showwarning("警告", "未找到 炼魂按钮")
        return
    # win_tool.send_input_mouse_left_click(xy[0] + 2, xy[1] + 3)
    win_tool.send_mouse_left_click(hwnd, xy[0] + 2, xy[1] + 3)

    # 更新炼魂 flag
    lian_hun_flag = new_flag

    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 炼魂完成
    dao2_common.say_hwnd(hwnd, f"{zb} 炼魂完成")


def exercise(hwnd, delay, zb):
    global is_run
    global lian_hun_flag
    global cheng_zhang_level

    position = ["1112,1023", "1020,1078"]
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
    find_daocaoren_count = 0
    while is_run:
        find_daocaoren_count += 1
        dao2_common.camera_top(hwnd)
        time.sleep(3)
        dao2_common.activity_window(hwnd)

        # win_tool.send_key("tab")
        win_tool.send_key_to_window_frequency(hwnd, "tab")
        time.sleep(0.3)
        if None is not resurgence(hwnd):
            return "is_resurgence"

        xy2 = dao2_common.find_pic(hwnd, "img/muye_daocaoren.bmp", 300, 0, w - 20, int(h * 0.3))
        if None is xy2:
            time.sleep(0.3)
            continue

        # 找10次还没找到稻草人，退出重跑
        if 10 <= find_daocaoren_count:
            return "not find daocaoren"

        # 找到稻草人，打断
        break

    new_flag = ""
    exe_count = 1
    # 攻击稻草人
    while is_run:
        win_tool.send_key_to_window(hwnd, "1")
        exe_count += 1
        time.sleep(float(delay))

        if None is not resurgence(hwnd):
            return "is_resurgence"

        # 进行检测，防止打死稻草人或者被人捣乱推出擂台
        if 0 != exe_count and exe_count % 2 == 0:
            dao2_common.activity_window(hwnd)
            # dao2_common.say_hwnd(hwnd, f"第{exe_count}次，检测擂台")

            xy2 = dao2_common.find_pic(hwnd, "img/muye_daocaoren.bmp", 300, 0, w - 20, int(h * 0.3))
            if None is xy2:
                # win_tool.send_key("tab")
                win_tool.send_key_to_window_frequency(hwnd, "tab")
                time.sleep(0.35)
                # 如果还是没有稻草人，重新跑
                xy3 = dao2_common.find_pic(hwnd, "img/muye_daocaoren.bmp", 300, 0, w - 20, int(h * 0.3))
                if None is xy3:
                    return "not find daocaoren"

        # 每练习  次，就打开装备检测一下需不需要炼魂
        if 0 != exe_count and exe_count % 5 == 0:
            
            if "成长等级：60" == lian_hun_flag:
                log3.logger.info(f"不需要炼魂 lian_hun_flag={lian_hun_flag}")
                continue

            # 关闭 6 点的弹窗
            dao2_common.close_6_oclock_dialog(hwnd)

            # 找成长等级
            new_flag = get_lian_hun_new_flag(hwnd, zb)
            dao2_common.say_hwnd(hwnd, f"牧野练副武后台版 第{exe_count}次，检测炼魂 lian_hun_flag={lian_hun_flag}， new_flag={new_flag}")
            if "" == new_flag:
                log3.logger.info(f"检测成长等级失败 new_flag={new_flag}")
                continue

            if lian_hun_flag == new_flag:
                log3.console(f"不需要炼魂 lian_hun_flag={lian_hun_flag}")
                continue

            if "成长等级：20" == new_flag:
                # 打断循环，去炼魂
                break

            if "成长等级：40" == new_flag:
                # 打断循环，去炼魂
                break

            if "成长等级：60" == new_flag:
                # 打断循环，去炼魂
                break

    if None is not resurgence(hwnd):
        return "is_resurgence"

    # 已经要炼魂
    dao2_common.close_zhuangbei(hwnd)
    return lian_hun(hwnd, zb, new_flag)


check_die_count = 0


# 复活
def resurgence(hwnd):
    global die_count
    global check_die_count

    check_die_count += 1
    xy = dao2_common.is_die_dian(hwnd, check_die_count)
    if None is xy:
        return None
    die_count += 1
    dao2_common.say_hwnd(hwnd, f"画个圈圈诅咒你 9_9 死亡次数={die_count}")

    time.sleep(1)
    # win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
    win_tool.send_mouse_left_click(hwnd, xy[0] + 5, xy[1] + 5)
    time.sleep(5)
    return xy




