import time

import gamelib
from MSN import win_tool
from pmcWinTool.shanhetuzhiBox import app_const
import random

is_run_auto_zhenyingzhan = False
is_run_auto_longzhuashou = False
is_run_auto_xianqi = False
is_run_auto_shengji = False
is_run_auto_shengxiandahui = False
is_run_auto_taichu = False
is_run_auto_xiandian = False
is_run_auto_zhuanshu= False
is_run_auto_zhanchangyiji= False

shuaxin_location = None
tiaozhanboss_location = None
dabaoboss_location = None

shuaxin_count = 0


def shuaxin(hwnd):
    w, h = gamelib.win_tool.get_win_w_h()
    global shuaxin_location
    if shuaxin_location is None:
        shuaxin_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/shuaxin.png", 0, 0, w * 0.3, h * 0.3,
                                                                 threshold=0.9, debug=False)
    win_tool.send_mouse_left_click(hwnd, shuaxin_location[0], shuaxin_location[1], False)
    global shuaxin_count
    shuaxin_count += 1
    gamelib.log3.console(f'刷新次数: {shuaxin_count}')


def crash_reboot(hwnd):
    w, h = gamelib.win_tool.get_win_w_h()
    location = gamelib.find_pic.find_image_in_window(hwnd, "./img/tiaozhanboss.png", w * 0.75, 0,
                                                     w, h * 0.45, 0.9, False)
    if location is None:
        # 卡住了
        gamelib.log3.console(f'crash_reboot 卡住刷新')
        shuaxin(hwnd)
        time.sleep(8)
        close_dialog_xianwang(hwnd)
        return True
    return False


def is_bengkui(hwnd):
    w, h = gamelib.win_tool.get_win_w_h()
    location = gamelib.find_pic.find_image_in_window(hwnd, "./img/bengkui.png", w * 0.2, 0.2 * h, w * 0.7, h * 0.7,
                                                     threshold=0.9, debug=False)
    if location is None:
        return False
    return True


def run_auto_zhenyingzhan():
    w, h = gamelib.win_tool.get_win_w_h()
    # 示例：查找 Chrome 窗口中的图片
    window_handles = gamelib.win_tool.get_all_window_handles_by_name(app_const.window_name)
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return

    global is_run_auto_zhenyingzhan
    while is_run_auto_zhenyingzhan:
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/lijifuhuo.png", w * 0.15, h * 0.2, w * 0.9, h,
                                                         threshold=0.9,
                                                         debug=False)
        if location is None:
            time.sleep(1)
            continue

        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(1)

        shenjiang_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/shenjiang.png", w * 0.5, h * 0.5,
                                                                   w * 0.9, h, threshold=0.9,
                                                                   debug=False)
        if shenjiang_location is None:
            time.sleep(1)
            continue
        win_tool.send_mouse_left_click(hwnd, shenjiang_location[0] + 20, location[1] - 150)


def run_auto_xianqi():
    w, h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name(app_const.window_name)
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return

    global is_run_auto_xianqi

    kuafu_location = None
    while is_run_auto_xianqi and kuafu_location is None:
        # 找跨服战场
        kuafu_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/kuafuzhanchan.png", w * 0.5, 0, w, h * 0.6,
                                                               0.8, False)
        if kuafu_location is None:
            time.sleep(2)
            continue

    # 跨服战场
    win_tool.send_mouse_left_click(hwnd, kuafu_location[0], kuafu_location[1])
    time.sleep(1)
    xian_location = None
    while is_run_auto_xianqi and xian_location is None:
        # 找仙骑
        xian_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/xianqi.png", w * 0.5, 0, w, h * 0.8, 0.9,
                                                              False)
        if xian_location is None:
            time.sleep(2)
            continue

    # 仙骑
    win_tool.send_mouse_left_click(hwnd, xian_location[0], xian_location[1])
    time.sleep(1)
    tiaozhan_location = None
    while is_run_auto_xianqi and tiaozhan_location is None:
        tiaozhan_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/qianwangtiaozhan.png", w * 0.5, h * 0.1,
                                                                  w, h * 0.8, 0.9, False)
        if tiaozhan_location is None:
            time.sleep(2)
            continue

    while is_run_auto_xianqi:
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/close.png", w * 0.5, h * 0.15, w * 0.95, h * 0.75,
                                                         0.9, False)
        if location is None:
            time.sleep(2)
            continue
        else:
            break

    while is_run_auto_xianqi:
        # 不在仙骑地图，进入
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/xianqiditu.png", w * 0.75, 0, w, h * 0.25, 0.9,False)
        if location is None:
            # 跨服战场
            win_tool.send_mouse_left_click(hwnd, kuafu_location[0], kuafu_location[1])
            time.sleep(1)

            # 仙骑
            win_tool.send_mouse_left_click(hwnd, xian_location[0], xian_location[1])
            time.sleep(1)

            # 前往挑战
            win_tool.send_mouse_left_click(hwnd, tiaozhan_location[0], tiaozhan_location[1])
            time.sleep(1)

        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/anquanfuhuo.png", w * 0.2, h * 0.15, w * 0.8,
                                                         h * 0.85, 0.9, False)
        if location is None:
            time.sleep(2)
            continue

        # 复活
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(2)

        # 跨服战场
        win_tool.send_mouse_left_click(hwnd, kuafu_location[0], kuafu_location[1])
        time.sleep(1)

        # 仙骑
        win_tool.send_mouse_left_click(hwnd, xian_location[0], xian_location[1])
        time.sleep(1)

        # 前往挑战
        win_tool.send_mouse_left_click(hwnd, tiaozhan_location[0], tiaozhan_location[1])
        time.sleep(1)


def qie_tu(hwnd, scroll_amount):
    w, h = gamelib.win_tool.get_win_w_h()
    # win_tool.scroll_mouse_wheel_at(hwnd, location[0], location[1], -360)
    # time.sleep(1)
    # win_tool.move_mouse(dabaoboss_location[0], dabaoboss_location[1] + 80)
    # time.sleep(1)
    # win_tool.scroll_mouse_up(scroll_amount)
    # time.sleep(1)
    # win_tool.mouse_left_click()

    global tiaozhanboss_location
    win_tool.send_mouse_left_click(hwnd, tiaozhanboss_location[0], tiaozhanboss_location[1], False)
    time.sleep(1)

    global dabaoboss_location
    global is_run_auto_shengji
    while is_run_auto_shengji and dabaoboss_location is None:
        if dabaoboss_location is None:
            dabaoboss_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/dabaoboss.png", w * 0.2, 0.2 * h,
                                                                       w * 0.65, h * 0.65, 0.9, False)
        if dabaoboss_location is None:
            time.sleep(1)
            continue

    # 后台移动
    win_tool.drag_window(hwnd, dabaoboss_location[0], dabaoboss_location[1] + 80, dabaoboss_location[1] + scroll_amount,
                         6)
    time.sleep(1)

    win_tool.send_mouse_left_click(hwnd, dabaoboss_location[0], dabaoboss_location[1] + 80, False)

    time.sleep(1)
    # 进入地图
    # win_tool.move_mouse(int(w*0.45), int(h*0.65))
    if 2 == random.randint(1, 2):
        win_tool.send_mouse_left_click(hwnd, int(w * 0.45), int(h * 0.65), False)
    else:
        win_tool.send_mouse_left_click(hwnd, int(w * 0.45), int(h * 0.65) + 50, False)
    time.sleep(1)


# run_auto_shengji 后台刷图
def run_auto_shengji():
    w, h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name(app_const.window_name)
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return

    # win_tool.activate_window(hwnd)

    # 步长
    # scroll_amount_step = 160
    # scroll_amount_init = 160*40 # 第一张图
    # scroll_amount_rollback = 160*30 # 最后一张图
    # scroll_amount = scroll_amount_init

    scroll_amount_step = 10
    scroll_amount_init = scroll_amount_step * 20  # 第一张图
    scroll_amount_rollback = scroll_amount_step * 10  # 最后一张图
    scroll_amount = scroll_amount_init

    suiji_max_count = 3
    global is_run_auto_shengji

    suiji_location = None
    while is_run_auto_shengji and suiji_location is None:
        suiji_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/suiji8.png", w * 0.5, h * 0.6,
                                                               w * 0.9, h, 0.9, False)
        if suiji_location is None:
            time.sleep(1)
            continue

    global tiaozhanboss_location

    while is_run_auto_shengji and tiaozhanboss_location is None:
        tiaozhanboss_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/tiaozhanboss.png", w * 0.5, 0,
                                                                      w, h * 0.5, 0.9, False)
        if tiaozhanboss_location is None:
            time.sleep(1)
            continue

    shuatu_count = 0
    while is_run_auto_shengji:
        qie_tu(hwnd, scroll_amount)

        suiji_count = 0
        while suiji_count is not suiji_max_count and is_run_auto_shengji:
            # 每 ？ 随机一次
            if is_bengkui(hwnd):
                shuaxin(hwnd)
                time.sleep(9)
                close_dialog_xianwang(hwnd)
            else:
                time.sleep(7)
            win_tool.send_mouse_left_click(hwnd, suiji_location[0], suiji_location[1], False)
            suiji_count = suiji_count + 1


        scroll_amount = scroll_amount - scroll_amount_step
        if scroll_amount < scroll_amount_rollback:
            scroll_amount = scroll_amount_init

        shuatu_count += 1
        # 崩溃自动刷新
        if is_bengkui(hwnd):
            shuaxin(hwnd)
            time.sleep(9)
            close_dialog_xianwang(hwnd)
        else:
            if crash_reboot(hwnd):
                print('crash_reboot')
            elif shuatu_count % 20 == 0:
                shuaxin(hwnd)
                time.sleep(9)
                close_dialog_xianwang(hwnd)
        gamelib.log3.console(f'后台刷图: {shuatu_count} 次')


def qie_tu_v2(hwnd, scroll_amount, floor):
    w, h = gamelib.win_tool.get_win_w_h()
    global tiaozhanboss_location
    global dabaoboss_location

    if tiaozhanboss_location is None:
        tiaozhanboss_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/tiaozhanboss.png", w * 0.5, 0,
                                                                      w, h * 0.5, 0.9, False)
    if tiaozhanboss_location is None:
        return

    win_tool.send_mouse_left_click(hwnd, tiaozhanboss_location[0], tiaozhanboss_location[1])
    time.sleep(1)

    if dabaoboss_location is None:
        dabaoboss_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/dabaoboss.png", w * 0.1, 0.1 * h,
                                                                   w * 0.8, h * 0.7, 0.9, False)

    if dabaoboss_location is None:
        return

    # win_tool.scroll_mouse_wheel_at(hwnd, location[0], location[1], -360)
    # time.sleep(1)
    win_tool.move_mouse(dabaoboss_location[0], dabaoboss_location[1] + 80)
    time.sleep(1)
    win_tool.scroll_mouse_up(scroll_amount)
    time.sleep(1)
    win_tool.mouse_left_click()
    time.sleep(1)
    # 进入地图
    # win_tool.move_mouse(int(w*0.45), int(h*0.65))
    if 1 == floor:
        win_tool.send_mouse_left_click(hwnd, int(w * 0.45), int(h * 0.65))
    else:
        win_tool.send_mouse_left_click(hwnd, int(w * 0.45), int(h * 0.65) + 50)
    time.sleep(1)


def close_dialog_xianwang(hwnd):
    w, h = gamelib.win_tool.get_win_w_h()
    location = gamelib.find_pic.find_image_in_window(hwnd, "./img/close_dialog_xianwang.png", w * 0.55, h * 0.2,
                                                           w * 0.9, h*0.7, 0.9, False)
    if location is None:
        return False
    win_tool.send_mouse_left_click(hwnd, location[0], location[1], False)
    time.sleep(0.05)
    print("关闭仙王弹窗 close_dialog_xianwang")
    return True


def run_auto_shengji_v2():
    w, h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name(app_const.window_name)
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return

    win_tool.activate_window(hwnd)

    # 步长
    scroll_amount_step = 160
    scroll_amount_init = 160 * 35  # 第一张图
    scroll_amount_rollback = 160 * 20  # 最后一张图
    scroll_amount = scroll_amount_init

    floor = 1
    shuatu_count = 0
    suiji_max_count = 4

    global is_run_auto_longzhuashou

    suiji_location = None
    while is_run_auto_longzhuashou and suiji_location is None:
        suiji_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/suiji8.png", w * 0.5, h * 0.6,
                                                               w * 0.9, h, 0.9, False)
        if suiji_location is None:
            time.sleep(1)
            continue

    while is_run_auto_longzhuashou:
        qie_tu_v2(hwnd, scroll_amount, floor)

        suiji_count = 0

        while suiji_count is not suiji_max_count and is_run_auto_longzhuashou:
            if is_bengkui(hwnd):
                shuaxin(hwnd)
                time.sleep(9)
                close_dialog_xianwang(hwnd)
            else:
                # 每 ？ 随机一次
                time.sleep(7)
            win_tool.send_mouse_left_click(hwnd, suiji_location[0], suiji_location[1])
            suiji_count = suiji_count + 1

        scroll_amount = scroll_amount - scroll_amount_step
        if scroll_amount < scroll_amount_rollback:
            scroll_amount = scroll_amount_init
            if 1 == floor:
                floor = 2
            else:
                floor = 1

        shuatu_count = shuatu_count + 1
        # 崩溃自动刷新
        if is_bengkui(hwnd):
            shuaxin(hwnd)
            time.sleep(9)
            close_dialog_xianwang(hwnd)
        else:
            if crash_reboot(hwnd):
                print('crash_reboot')
            elif shuatu_count % 20 == 0:
                shuaxin(hwnd)
                time.sleep(9)
                close_dialog_xianwang(hwnd)

        gamelib.log3.console(f'后台刷图: {shuatu_count} 次')
        win_tool.send_key("ctrl", 1)


def run_auto_shengxiandahui():
    w, h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name(app_const.window_name)
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return

    global is_run_auto_shengxiandahui
    while is_run_auto_shengxiandahui:
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/lingqujiangli.png", w * 0.3, h * 0.3, w * 0.8,
                                                         h * 0.8, 0.9, False)
        if location is not None:
            win_tool.send_mouse_left_click(hwnd, location[0], location[1], False)
            time.sleep(1)

        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/pipeiduishou.png", w * 0.3, h * 0.3, w * 0.8,
                                                         h * 0.8, 0.9, False)
        if location is None:
            time.sleep(2)
            continue
        win_tool.send_mouse_left_click(hwnd, location[0], location[1], False)
        time.sleep(2)


def run_auto_taichu():
    w, h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name(app_const.window_name)
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return

    global is_run_auto_taichu

    suiji_location = None
    while is_run_auto_taichu and suiji_location is None:
        suiji_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/suiji8.png", w * 0.5, h * 0.6,
                                                               w * 0.9, h, 0.9, False)
        if suiji_location is None:
            time.sleep(1)
            continue

    kuafu_location = None
    while is_run_auto_taichu and kuafu_location is None:
        # 找跨服战场
        kuafu_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/kuafuzhanchan.png", w * 0.7, h * 0.1,
                                                               w * 0.95, h * 0.6, 0.8, False)
        if kuafu_location is None:
            time.sleep(2)
            continue

    is_open_kuafu = False
    # win_tool.move_mouse(kuafu_location[0], kuafu_location[1])
    taichu_location = None
    while is_run_auto_taichu and taichu_location is None:
        # 找太初战场
        taichu_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/taichuzhanchang.png", w * 0.2, h * 0.2,
                                                                w * 0.8, h * 0.8, 0.8, False)
        if taichu_location is None:
            time.sleep(1)
            win_tool.send_mouse_left_click(hwnd, kuafu_location[0], kuafu_location[1])
            time.sleep(1)
            is_open_kuafu = True
            continue

    while is_run_auto_taichu:
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/taichuzhanchangditu.png", w * 0.7, 0, w, h * 0.8,
                                                         0.9, False)
        if location is None:
            # 说明不在太初战场，检测是不是崩溃
            if is_bengkui(hwnd):
                shuaxin(hwnd)
                time.sleep(9)
                close_dialog_xianwang(hwnd)
            # 进入太初战场
            if is_open_kuafu:
                is_open_kuafu = False
            else:
                win_tool.send_mouse_left_click(hwnd, kuafu_location[0], kuafu_location[1], False)
                time.sleep(1)
            win_tool.send_mouse_left_click(hwnd, taichu_location[0], taichu_location[1], False)
            time.sleep(1)
            location = gamelib.find_pic.find_image_in_window(hwnd, "./img/lijiqianwang.png", w * 0.25, h * 0.25,
                                                             w * 0.75,
                                                             h * 0.75, 0.9, False)
            if location is None:
                time.sleep(1)
                continue
            win_tool.send_mouse_left_click(hwnd, location[0], location[1], False)
            time.sleep(1)

        # 随机
        win_tool.send_mouse_left_click(hwnd, suiji_location[0], suiji_location[1], False)
        time.sleep(6)


def run_auto_xiandian():
    w, h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name(app_const.window_name)
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return


    global is_run_auto_xiandian
    while is_run_auto_xiandian:
        # 不在 仙殿也不在内殿，点击进入仙殿
        neidian_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/neidianditu.png", w * 0.75, 0, w, h * 0.8,
                                                                 0.9, False)

        waidian_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/qingtongxiandianditu.png", w * 0.75, 0, w,
                                                                 h * 0.8,0.9, False)
        if neidian_location is None and waidian_location is None:
            # 进入
            location = gamelib.find_pic.find_image_in_window(hwnd, "./img/xiandian.png", w * 0.7,
                                                                     0, w,h * 0.7,0.8, False)
            if location is None:
                time.sleep(1)
                continue
            # 点击
            win_tool.send_mouse_left_click(hwnd, location[0], location[1], False)
            time.sleep(1)
            # 确定进入
            location = gamelib.find_pic.find_image_in_window(hwnd, "./img/dianjiqianwangxiandian.png", w * 0.7,
                                                                     h*0.1, w,h * 0.7,0.8, False)
            if location is None:
                time.sleep(1)
                continue
            win_tool.send_mouse_left_click(hwnd, location[0], location[1], False)
            time.sleep(3)
            continue

        if waidian_location:
            # 在外殿，去内殿
            location = gamelib.find_pic.find_image_in_window(hwnd, "./img/zhanlingneidian.png", w * 0.8,
                                                                     h*0.2, w, h * 0.3,0.8, False)
            if location is None:
                time.sleep(1)
                continue
            win_tool.send_mouse_left_click(hwnd, location[0], location[1], False)
            time.sleep(10)
            continue

        if neidian_location:
            # 已在内殿
            print('已经在内殿')
            shenjiang_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/shenjiang.png", w * 0.5, h * 0.5,
                                                                       w * 0.9, h, threshold=0.9,
                                                                       debug=False)
            if shenjiang_location is None:
                time.sleep(1)
                continue
            win_tool.send_mouse_left_click(hwnd, shenjiang_location[0] + 20, location[1] - 150)

        time.sleep(1)


def run_auto_zhuanshu():
    w, h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name(app_const.window_name)
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return
    global is_run_auto_zhuanshu
    global tiaozhanboss_location

    while is_run_auto_zhuanshu and tiaozhanboss_location is None:
        tiaozhanboss_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/tiaozhanboss.png", w * 0.5, 0,
                                                                      w, h * 0.5, 0.9, False)
        if tiaozhanboss_location is None:
            time.sleep(1)
            continue
    count = 0
    while is_run_auto_zhuanshu:
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/zhuanshu_ditu.png", w * 0.75, 0, w, h * 0.25, 0.9,
                                                         False)
        if location is None:
            # 不在地图里，进入地图
            zhuanshu_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/zhuanshu.png", w * 0.5, h*0.15, w*0.9, h * 0.8, 0.9, False)
            if zhuanshu_location is None:
                win_tool.send_mouse_left_click(hwnd, tiaozhanboss_location[0], tiaozhanboss_location[1], False)
                time.sleep(1)
                continue
            win_tool.send_mouse_left_click(hwnd, zhuanshu_location[0], zhuanshu_location[1], False)
            time.sleep(1)

            # 找首杀
            shousha_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/yishousha.png", w * 0.15, h*0.1, w*0.65, h * 0.6,0.9,False)
            if shousha_location is None:
                time.sleep(1)
                continue

            if count == 4:
                count = 0
            win_tool.send_mouse_left_click(hwnd, shousha_location[0], shousha_location[1] + count * 80, False)
            time.sleep(1)

            qianwangtiaozhan_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/zhuanshu_qianwangtiaozhan.png", w * 0.3, h * 0.3,
                                                                         w * 0.8, h * 0.8, 0.9, False)
            if qianwangtiaozhan_location is None:
                time.sleep(1)
                continue
            win_tool.send_mouse_left_click(hwnd, qianwangtiaozhan_location[0], qianwangtiaozhan_location[1], False)
            time.sleep(1)

            zhaunshu_queding_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/zhaunshu_queding.png", w * 0.3, h * 0.3,
                                                                         w * 0.8, h * 0.8, 0.9, False)
            if zhaunshu_queding_location is not None:
                win_tool.send_mouse_left_click(hwnd, zhaunshu_queding_location[0], zhaunshu_queding_location[1], False)
                time.sleep(1)

            count = count + 1
        else:
            time.sleep(1)


def run_auto_zhanchangyiji():
    w, h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name(app_const.window_name)
    print(window_handles)
    hwnd = window_handles[0]
    if hwnd == 0:
        print("❌ 未找到 Chrome 窗口，请确认标题")
        return
    global is_run_auto_zhanchangyiji
    kuafu_location = None
    while is_run_auto_zhanchangyiji and kuafu_location is None:
        kuafu_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/kuafuzhanchan.png", w * 0.7, 0,
                                                                      w, h * 0.5, 0.9, False)
        if kuafu_location is None:
            time.sleep(1)
            continue

    while is_run_auto_zhanchangyiji:
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/yijiditu.png", w * 0.75, 0, w, h * 0.25, 0.9,
                                                         False)
        if location is None:
            # 不在地图里，进入地图
            zhanchangyiji_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/zhanchangyiji.png", w * 0.5, h*0.15, w*0.9, h * 0.8, 0.9, False)
            if zhanchangyiji_location is None:
                win_tool.send_mouse_left_click(hwnd, kuafu_location[0], kuafu_location[1], False)
                time.sleep(1)
                continue
            win_tool.send_mouse_left_click(hwnd, zhanchangyiji_location[0], zhanchangyiji_location[1], False)
            time.sleep(1)

            # 去挑战
            qianwangtiaozhan_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/qianwangtiaozhan_yiji.png", w * 0.3, h * 0.3,
                                                                         w * 0.8, h * 0.9, 0.9, False)
            if qianwangtiaozhan_location is None:
                time.sleep(1)
                continue
            win_tool.send_mouse_left_click(hwnd, qianwangtiaozhan_location[0], qianwangtiaozhan_location[1], False)
            time.sleep(1)

            zhaunshu_queding_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/zhaunshu_queding.png", w * 0.3, h * 0.3,
                                                                         w * 0.8, h * 0.8, 0.9, False)
            if zhaunshu_queding_location is not None:
                win_tool.send_mouse_left_click(hwnd, zhaunshu_queding_location[0], zhaunshu_queding_location[1], False)
                time.sleep(1)
        else:
            time.sleep(1)