import random
import threading
import time

import dao2_common
import win_tool
import log3
import traceback
import ocr_tool
import os
from datetime import datetime


# 收费
money = 5


say_start_list = [",我很欣赏你的勇气,我接受你的挑战!", ",让我见识你的武艺吧!",
                  ",你知道我的刀有多快吗?", "你会后悔的!",
                  "你对真正的实力一无所知！", "受死吧！"]

rand_say_list = ["你知道新手村吗?,我很喜欢那里,可惜那里有人养狗,你知道的,我最怕狗了.",
                 "潇湘夜雨 are a romantic gang,可惜那里只要武功高强的侠士,他们看不上像我这样的世外高人.",
                 "你认识童尼么?,对,就是那个每天遛萌新的家伙.",
                 "嗯,今天生意不太好,怎么都没人打 6次 了呢?",
                 "让我翻翻账本,今天有好几个赖账的,该让他们见识到我的刀有多锋利.",
                 "我得走了,我必须去摧毁大石村的文物--<<死亡空间：坍塌>>",
                 "那些赖账的，我诅咒他们出门踩 Dog 屎"]

black_list = {
    "十把大斧头": True,
    "一剑破日": True,
    "阳顶天阳大侠": True,
    "听说你很头瓷。": True,
    "林亦杨": True,
    "血剑孤狼": True,
              }

pay_list = {}


point_xy = "656,516"

is_run = False
lock = threading.Lock()
w, h = win_tool.get_win_w_h()
skill_arr = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
die_count = 0
current_pk_name = ""
current_pk_finish = False
current_deal_name = ""
current_deal_finish = ""
close_6_oclock = False


# 复活
def resurgence(hwnd):
    global die_count
    xy = dao2_common.is_die(hwnd)
    if None is xy:
        return None
    die_count += 1
    dao2_common.say_hwnd(hwnd, f"凶手,我已将你的名字记在生死簿上,厄运将与你如影随形.")
    time.sleep(0.6)
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
    return "resurgence"


def run_six_contest(hwnd):
    with lock:
        t = threading.Thread(target=contest, args=(hwnd,), daemon=True)
        t.start()


def contest(hwnd):
    while is_run:
        # 去瓦当
        try:
            is_ok = dao2_common.tu_dun_wa_dang(hwnd)
        except Exception as e:
            is_ok = traceback.format_exc()
            log3.logger.error(is_ok)

        if "" != is_ok:
            time.sleep(5)
            continue

        time.sleep(7)
        win_tool.send_key_to_window_frequency(hwnd, "w", 3)
        time.sleep(3)

        dao2_common.navigation_x_y(hwnd, point_xy)
        time.sleep(15)
        win_tool.send_key_to_window_frequency(hwnd, "ctrl", 1)
        time.sleep(15)
        # dao2_common.camera_focus(hwnd, 1200)

        if "resurgence" == resurgence(hwnd):
            time.sleep(1)
            continue

        if "resurgence" == six_contest(hwnd):
            # 复活
            time.sleep(1)
            continue


def six_contest(hwnd):
    global skill_arr
    global is_run
    global current_pk_name
    global current_pk_finish
    global current_deal_name
    global close_6_oclock

    # 1.在副本就战斗，离开副本时发言 xxx 请付钱
    # 2.
    say_count = 0
    win_tool.send_key_to_window_frequency(hwnd, "x")
    time.sleep(0.15)

    while is_run:

        # 关闭 6 点的弹窗
        now = datetime.now()
        if now.hour == 6 and now.minute == 0 and close_6_oclock:
            dao2_common.close_6_oclock_dialog(hwnd)
            close_6_oclock = False
        else:
            close_6_oclock = True

        if "resurgence" == resurgence(hwnd):
            return "resurgence"

        # 交易通知
        xy = dao2_common.find_pic(hwnd, "img/tongzhi_deal.bmp", int(w * 0.35), int(h * 0.22), int(w * 0.7),
                                  int(h * 0.9))
        if None is not xy:
            deal(hwnd, xy)
            deal_msg(hwnd)
            time.sleep(0.1)

        # 战斗判断
        is_f = fight(hwnd)
        if is_f:
            # 比武完成
            is_deal = ""
            for k in range(80):
                if k % 15 == 0:
                    # win_tool.send_mouse_left_click(hwnd, int(w / 2), int(h * 0.57))
                    dao2_common.open_navigation_and_click(hwnd)
                    time.sleep(0.05)
                    win_tool.send_key_to_window_frequency(hwnd, "x")
                    time.sleep(0.1)
                    dao2_common.say_hwnd(hwnd, f"{current_pk_name} 交易我{money}j。")
                time.sleep(0.2)
                # 交易通知
                xy = dao2_common.find_pic(hwnd, "img/tongzhi_deal.bmp", int(w * 0.35), int(h * 0.22), int(w * 0.7),
                                          int(h * 0.9))
                if None is xy:
                    continue

                if deal(hwnd, xy):
                    is_deal = deal_msg(hwnd)
                    break

            if "" == is_deal:
                dao2_common.say_hwnd(hwnd, f"{current_pk_name} 你个老赖,玩完不给钱,画圈圈诅咒你。")
                time.sleep(0.2)

        # 接受比武通知
        xy = dao2_common.find_pic(hwnd, "img/tongzhi_biwu.bmp", int(w * 0.35), int(h * 0.22), int(w*0.7), int(h * 0.9))
        if None is xy:
            # 没有比武通知
            if say_count % 100 == 0:
                # win_tool.send_mouse_left_click(hwnd, int(w/2), int(h*0.57))
                dao2_common.open_navigation_and_click(hwnd)
                time.sleep(0.05)
                win_tool.send_key_to_window_frequency(hwnd, "x")
                time.sleep(0.1)
                dao2_common.say_hwnd(hwnd, f"试炼擂台 6次 自助,点我开始擂台,收费 {money}j,玩完后请自觉交易,谢谢.")
                time.sleep(0.1)
            else:
                seed = int(time.time() * 1000) ^ os.getpid()
                random.seed(seed)
                r = random.randint(0, len(rand_say_list) * 500)
                if r < len(rand_say_list):
                    time.sleep(0.1)
                    dao2_common.say_hwnd(hwnd, rand_say_list[r])
                    time.sleep(0.1)

            time.sleep(0.25)
            say_count += 1
            continue

        # 有比武通知,点击
        win_tool.send_mouse_left_click(hwnd, xy[0]+3, xy[1]+6)
        time.sleep(0.25)
        # 识图,找出名字
        s_arr = ocr_tool.capture_window_to_str(hwnd, int(w * 0.2), int(0.2 * h), int(w * 0.7), int(h * 0.8), "想与您")
        s_arr = s_arr.strip().split("\n")
        f_inx = s_arr[0].find("想与您")
        print(f_inx)
        print(s_arr[0][:f_inx])
        current_pk_name = s_arr[0][:f_inx]

        if "武艺" in s_arr[0]:
            dao2_common.say_hwnd(hwnd, f"{current_pk_name} 刀剑无眼，不要用你的性命开玩笑，请选择进入副本切磋")
            time.sleep(0.1)

            # 拒绝决斗
            xy = dao2_common.find_pic(hwnd, "img/btn_x.bmp", int(w * 0.2), int(0.15 * h), int(w * 0.75),
                                      int(h * 0.8), 0.8)
            win_tool.send_mouse_left_click(hwnd, xy[0] + 3, xy[1] + 6)
            time.sleep(0.5)
            continue

        # 检测黑名单
        if is_black(hwnd, current_pk_name):
            # 拒绝比武 btn_x
            xy = dao2_common.find_pic(hwnd, "img/btn_x.bmp", int(w * 0.2), int(0.15 * h), int(w * 0.75),
                                      int(h * 0.8), 0.8)
            win_tool.send_mouse_left_click(hwnd, xy[0] + 3, xy[1] + 6)
            time.sleep(0.5)
            continue

        dao2_common.say_hwnd(hwnd, f"{current_pk_name} {say_start_list[random.randint(0, len(say_start_list)-1)]}")
        time.sleep(0.3)

        # 同意进行比武
        xy = dao2_common.find_pic(hwnd, "img/btn_gouzi.bmp", int(w * 0.2), int(0.15 * h), int(w * 0.75), int(h * 0.8), 0.8)
        win_tool.send_mouse_left_click(hwnd, xy[0] + 3, xy[1] + 6)
        time.sleep(3)


def deal_msg(hwnd):
    global pay_list

    s_arr = ocr_tool.capture_window_to_str(hwnd, 0, int(0.5 * h), int(w * 0.65), h, "获得刀币")
    s_arr = s_arr.strip().split("\n")
    log3.logger.info(s_arr)
    if "" == s_arr[0]:
        dao2_common.say_hwnd(hwnd, f" {current_deal_name} 你个出生!,什么也没给。")
        return ""
    else:
        dao2_common.say_hwnd(hwnd, f"谢谢 {current_deal_name} 大侠,真乃乾坤楷模。")
        pay_list[current_deal_name] = True
    return s_arr[0]


def deal(hwnd, xy):
    global current_deal_finish
    global current_deal_name

    # 有交易通知,点击
    win_tool.send_mouse_left_click(hwnd, xy[0] + 3, xy[1] + 6)
    time.sleep(0.25)
    # 识图,找出名字
    s_arr = ocr_tool.capture_window_to_str(hwnd, int(w * 0.2), int(0.2 * h), int(w * 0.7), int(h * 0.8), "邀请您")
    s_arr = s_arr.strip().split("\n")
    f_inx = s_arr[0].find("邀请您")
    current_deal_name = s_arr[0][:f_inx]
    dao2_common.say_hwnd(hwnd, f"来吧 我得宝贝, {current_deal_name} ,我只要 {money}j")
    time.sleep(0.1)

    # 同意交易
    for _ in range(3):
        xy = dao2_common.find_pic(hwnd, "img/btn_gouzi.bmp", int(w * 0.2), int(0.15 * h), int(w * 0.75), int(h * 0.8), 0.8)
        if None is xy:
            time.sleep(0.3)
            continue
        win_tool.send_mouse_left_click(hwnd, xy[0] + 3, xy[1] + 6)
        time.sleep(0.3)

    # 找和字,向下偏移,锁定交易
    xy = dao2_common.find_pic(hwnd, "img/deal_he.bmp", 0, 0, int(w * 0.25), int(h * 0.9), 0.8)
    if None is xy:
        log3.logger.error(f"没找到 和 字")
        return False

    # 点击锁定交易
    s_d_x = xy[0] + 15
    s_d_y = xy[1] + 490
    win_tool.send_mouse_left_click(hwnd, s_d_x, s_d_y)
    time.sleep(0.1)

    # 点击 btn_deal
    for _ in range(50):
        btn_deal_xy = dao2_common.find_pic(hwnd, "img/btn_deal.bmp", 0, 0, int(w * 0.3), int(h * 0.9), 0.8)
        if None is btn_deal_xy:
            time.sleep(1)
            continue
        print(f"交易按钮 xy={btn_deal_xy}")
        # 没找到和字,说明交易窗口关了,交易窗口关了,才能确定交易完成 btn_deal_un  pk_6
        for _ in range(35):
            dao2_common.open_navigation_and_click(hwnd)
            time.sleep(0.1)
            win_tool.send_mouse_left_click(hwnd, btn_deal_xy[0] + 5, btn_deal_xy[1] + 5)
            time.sleep(0.1)

            xy = dao2_common.find_pic(hwnd, "img/deal_he.bmp", 0, 0, int(w * 0.25), int(h * 0.9), 0.8)
            if None is xy:
                dao2_common.esc_and_back(hwnd)
                current_deal_finish = True
                return True
        break

    xy = dao2_common.find_pic(hwnd, "img/deal_he.bmp", 0, 0, int(w * 0.25), int(h * 0.9), 0.8)
    if None is not xy:
        current_deal_finish = False
        dao2_common.esc_and_back(hwnd)
        log3.logger.info(f"关闭与 {current_deal_name} 的超时交易")

    return False


def fight(hwnd):
    global skill_arr
    global is_run
    global current_pk_name
    global current_pk_finish

    while is_run:
        # 在副本判断
        xy = dao2_common.find_pic(hwnd, "img/jingjichang_fuben.bmp", int(w * 0.7), int(h * 0.6), w - 10, h - 50, 0.8)
        if None is xy:
            return False

        time.sleep(2)

        # 敌人血条
        w_count = 0
        while is_run:
            xy = dao2_common.find_pic(hwnd, "img/diren_xuetiao.bmp", int(w * 0.25), 0, int(w * 0.75), int(h * 0.2), 0.8)
            if None is xy:
                # 不在副本,说明完成了
                if not is_fu_ben(hwnd):
                    return True
                win_tool.send_key_to_window(hwnd, "w", 0.1)
                time.sleep(0.1)
                w_count += 1
                if 1 == w_count:
                    dao2_common.esc_and_back(hwnd)
                    time.sleep(3)
                    dao2_common.camera_forward(hwnd)
                    time.sleep(2)
                elif 2 == w_count:
                    time.sleep(1)
                else:
                    dao2_common.camera_forward(hwnd)
                    time.sleep(0.15)
                    win_tool.send_key_to_window(hwnd, "tab")
                    time.sleep(0.15)
            else:
                break

        # 开始放技能
        skill_inx = 0
        while is_run:
            print(f"{hwnd} 攻击 {skill_arr[skill_inx]}")
            if (skill_inx+1) % 5 == 0:
                win_tool.send_key_to_window_frequency(hwnd, "w", 3)
                time.sleep(0.5)
                tong_yi(hwnd)

            win_tool.send_key_to_window(hwnd, skill_arr[skill_inx])
            time.sleep(0.5)
            skill_inx += 1
            if skill_inx == len(skill_arr):
                skill_inx = 0

            # 不在副本,说明完成了
            if not is_fu_ben(hwnd):
                return True


def is_black(hwnd, name):
    global black_list
    global pay_list

    if -1 == black_list.get(name, -1):
        return False
    # 检查支付
    if -1 != pay_list.get(name, -1):
        return False

    # 在黑名单 发言让他交罚款
    dao2_common.say_hwnd(hwnd, f"{name} 你因屡次赖账，已被列入失信名单，交 100j 可恢复正常。")
    time.sleep(0.1)
    return True


def is_fu_ben(hwnd):
    global current_pk_finish

    # 在副本判断
    xy = dao2_common.find_pic(hwnd, "img/jingjichang_fuben.bmp", int(w * 0.7), int(h * 0.6), w - 10, h - 50,
                              0.8)
    if None is xy:
        # 不在副本，打断循环
        current_pk_finish = True
        time.sleep(1.5)
        return False

    return True


# 继续切磋
def tong_yi(hwnd):
    is_ok = False
    for _ in range(3):
        xy = dao2_common.find_pic(hwnd, "img/btn_gouzi.bmp", int(w * 0.2), int(0.15 * h), int(w * 0.75), int(h * 0.8), 0.8)
        if None is xy:
            time.sleep(0.1)
            continue
        win_tool.send_mouse_left_click(hwnd, xy[0]+3, xy[1]+6)
        is_ok = True
    return is_ok



