import time

import gamelib
from MSN import win_tool
from pmcWinTool.shanhetuzhiBox import app_const

is_run_auto_zhenyingzhan = False
is_run_auto_longzhuashou = False
is_run_auto_xianqi = False
is_run_auto_shengji = False

shuaxin_location = None
tiaozhanboss_location = None
dabaoboss_location = None


shuaxin_count = 0

def shuaxin(hwnd):
    w, h = gamelib.win_tool.get_win_w_h()
    global shuaxin_location
    if shuaxin_location is None:
        shuaxin_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/shuaxin.png", 0, 0, w * 0.3, h*0.3,
                                                 threshold=0.9,debug=False)
    win_tool.send_mouse_left_click(hwnd, shuaxin_location[0], shuaxin_location[1], False)
    global shuaxin_count
    shuaxin_count += 1
    gamelib.log3.console(f'刷新次数: {shuaxin_count}')


def is_bengkui(hwnd):
    w, h = gamelib.win_tool.get_win_w_h()
    location = gamelib.find_pic.find_image_in_window(hwnd, "./img/bengkui.png", w*0.2, 0.2*h, w * 0.7, h * 0.7,
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
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/lijifuhuo.png",  w*0.15, h*0.2, w*0.9, h, threshold=0.9,
                                                         debug=False)
        if location is None:
            time.sleep(1)
            continue

        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(1)

        shenjiang_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/shenjiang.png",  w*0.5, h*0.5, w*0.9, h, threshold=0.9,
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
    while is_run_auto_xianqi:
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/anquanfuhuo.png", w*0.2, h*0.15, w*0.8, h*0.85, 0.9, False)
        if location is None:
            time.sleep(2)
            continue
        # 复活
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(2)
        # 找跨服战场
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/kuafuzhanchan.png", w*0.5, 0, w, h*0.6, 0.8, False)
        if location is None:
            time.sleep(2)
            continue
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(1)
        # 找仙骑
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/xianqi.png", w*0.5, 0, w, h*0.8, 0.9, False)
        if location is None:
            time.sleep(2)
            continue
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
        time.sleep(1)
        # 前往挑战
        location = gamelib.find_pic.find_image_in_window(hwnd, "./img/qianwangtiaozhan.png", w*0.5, h*0.1, w, h*0.8, 0.9, False)
        if location is None:
            time.sleep(2)
            continue
        win_tool.send_mouse_left_click(hwnd, location[0], location[1])
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
    win_tool.send_mouse_left_click(hwnd, tiaozhanboss_location[0], tiaozhanboss_location[1], True)
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
    win_tool.drag_window(hwnd, dabaoboss_location[0], dabaoboss_location[1] + 80, dabaoboss_location[1] + scroll_amount, 5)
    time.sleep(1)

    win_tool.send_mouse_left_click(hwnd, dabaoboss_location[0], dabaoboss_location[1] + 80, False)

    time.sleep(1)
    # 进入地图
    # win_tool.move_mouse(int(w*0.45), int(h*0.65))
    win_tool.send_mouse_left_click(hwnd, int(w*0.45), int(h*0.65), False)
    time.sleep(1)


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

    scroll_amount_step = 15
    scroll_amount_init = scroll_amount_step*30 # 第一张图
    scroll_amount_rollback = scroll_amount_step*20 # 最后一张图
    scroll_amount = scroll_amount_init

    suiji_max_count = 5

    suiji_location = None
    while suiji_location is None:
        suiji_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/suiji8.png", w * 0.5, h * 0.6,
                                                               w * 0.9, h, 0.9, False)
        if suiji_location is None:
            time.sleep(1)
            continue

    global tiaozhanboss_location

    while tiaozhanboss_location is None:
        tiaozhanboss_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/tiaozhanboss.png", w * 0.5, 0,
                                                     w, h * 0.5, 0.9, False)
        if tiaozhanboss_location is None:
            time.sleep(1)
            continue

    shuatu_count = 0
    global is_run_auto_shengji
    while is_run_auto_shengji:
        qie_tu(hwnd, scroll_amount)

        suiji_count = 0
        while suiji_count is not suiji_max_count and is_run_auto_shengji:
            # 每 ？ 随机一次
            time.sleep(8)
            win_tool.send_mouse_left_click(hwnd, suiji_location[0], suiji_location[1], False)
            suiji_count = suiji_count + 1

        scroll_amount = scroll_amount - scroll_amount_step
        if scroll_amount < scroll_amount_rollback:
            scroll_amount = scroll_amount_init

        # 崩溃自动刷新
        if is_bengkui(hwnd):
            shuaxin(hwnd)
            time.sleep(10)

        zhizunvip = gamelib.find_pic.find_image_in_window(hwnd, "./img/zhizunvip.png", w * 0.7, 0,
                                                               w, h*0.5, 0.9, False)
        if zhizunvip is None:
            gamelib.log3.console(f'没有在正常刷图: {shuatu_count}')
        else:
            shuatu_count += 1
            gamelib.log3.console(f'正常刷图: {shuatu_count} 次')

def qie_tu_v2(hwnd,scroll_amount):
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
    win_tool.send_mouse_left_click(hwnd, int(w*0.45), int(h*0.65))
    time.sleep(1)


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
    scroll_amount_init = 160*40 # 第一张图
    scroll_amount_rollback = 160*30 # 最后一张图
    scroll_amount = scroll_amount_init

    suiji_max_count = 6
    suiji_location = None
    global is_run_auto_longzhuashou
    while is_run_auto_longzhuashou:
        qie_tu_v2(hwnd, scroll_amount)

        suiji_count = 0
        while suiji_count is not suiji_max_count and is_run_auto_longzhuashou:
            # 每 ？ 随机一次
            time.sleep(8)
            if suiji_location is None:
                suiji_location = gamelib.find_pic.find_image_in_window(hwnd, "./img/suiji8.png", w * 0.5, h*0.6,
                                                                 w*0.9, h, 0.9, False)
            if suiji_location is None:
                return
            win_tool.send_mouse_left_click(hwnd, suiji_location[0], suiji_location[1])
            suiji_count = suiji_count + 1

        scroll_amount = scroll_amount - scroll_amount_step
        if scroll_amount < scroll_amount_rollback:
            scroll_amount = scroll_amount_init

        # 崩溃自动刷新
        if is_bengkui(hwnd):
            shuaxin(hwnd)
            time.sleep(10)