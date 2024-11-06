import time

import win32gui

import win_tool
import bg_find_pic_area
import threading
from tkinter import messagebox
import win32con
import win32api
import app_const
import traceback
import log3
import win32clipboard as clipboard
import ctypes
lock = threading.Lock()

scale = win_tool.get_screen_scale()
w, h = win_tool.get_win_w_h()


def find_pic_original(hwnd, img_name, x_offset, y_offset, width, height, threshold=0.7, is_desktop_handle=False):
    print(
        f"find_pic_original hwnd={hwnd} img_name={img_name} x_offset={x_offset}, y_offset={y_offset}, w={width}, h={int(height)}")
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path(img_name), x_offset, y_offset, width,
                                               height, threshold, is_desktop_handle)
    print(f"find_pic_original xy = {xy}")
    if None is xy:
        return None
    x = int(xy[0] + x_offset)
    y = int(xy[1] + y_offset)
    print(f"find_pic_original x={x}, y={y}")
    return int(x), int(y)


def find_pic(hwnd, img_name, x_offset, y_offset, width, height, threshold=0.7, is_desktop_handle=False):
    # print(f"find_pic hwnd={hwnd} img_name={img_name} x_offset={x_offset}, y_offset={y_offset}, w={width}, h={int(height)}")
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path(img_name), x_offset, y_offset, width,
                                               height, threshold, is_desktop_handle)
    # print(f"find_pic xy = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset)
    y = scale * (int(xy[1]) + y_offset)
    # print(f"find_pic x={x}, y={y}")
    return int(x), int(y)


# 是否死亡
def is_die(hwnd):
    xy = find_pic(hwnd, "img/huangquanzhilu.bmp", int(0.2*w), int(h*0.1), int(w * 0.7), int(h * 0.7))
    if None is xy:
        print(f"{hwnd}-检测死亡状态-未死亡")
        return None
    print(f"{hwnd}-检测死亡状态-已死亡")
    return xy


# 是否死亡（复活点）
def is_die_dian(hwnd):
    xy = find_pic(hwnd, "img/fuhuodianfuhuo.bmp", int(w * 0.2), int(h * 0.1), int(w * 0.7), int(h * 0.6))
    if None is xy:
        print(f"{hwnd}-检测死亡状态-未死亡")
        return None
    print(f"{hwnd}-检测死亡状态-已死亡")
    return xy


def find_lvse_shouzhang(hwnd):
    x_offset = 500
    y_offset = int(h * 0.2)
    print(f"find_lvse_shouzhang x_offset={x_offset}, y_offset={y_offset}, w={int(w * 0.7)}, h={int(h * 0.8)}")
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/lvse_shouzhang.bmp"), x_offset,
                                               y_offset, int(w * 0.7), int(h * 0.7))
    print(f"find_lvse_shouzhang xy = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset)
    y = scale * (int(xy[1]) + y_offset)
    print(f"find_lvse_shouzhang x={x}, y={y}")
    return x, y


# find_cao_yao 找草药
def find_cao_yao(hwnd, img_name):
    x_offset = int(w * 0.2)
    y_offset = int(h * 0.1)
    xy = bg_find_pic_area.find_image_in_window(hwnd, img_name, x_offset, y_offset, int(w * 0.8), int(h * 0.7))
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset) + 10
    y = scale * (int(xy[1]) + y_offset) + 35
    print(f"find_da_huang x={x}, y={y}")
    return x, y


def find_ma_huang_list(hwnd):
    arr = [win_tool.resource_path("img/mahuang1.bmp"), win_tool.resource_path("img/mahuang2.bmp"),
           win_tool.resource_path("img/mahuang3.bmp"), win_tool.resource_path("img/mahuang4.bmp")]
    for i in arr:
        xy = find_cao_yao(hwnd, i)
        if None is not xy:
            return xy
    return None


def find_gan_cao_list(hwnd):
    arr = [win_tool.resource_path("img/gancao1.bmp"), win_tool.resource_path("img/gancao2.bmp"),
           win_tool.resource_path("img/gancao3.bmp"), win_tool.resource_path("img/gancao4.bmp"),
           win_tool.resource_path("img/gancao5.bmp")]
    for i in arr:
        xy = find_cao_yao(hwnd, i)
        if None is not xy:
            print(f"find_gan_cao_list 找到甘草={xy}")
            return xy
    return None


def find_da_huang_list(hwnd):
    arr = [win_tool.resource_path("img/dahuang.bmp"), win_tool.resource_path("img/dahuang2.bmp"),
           win_tool.resource_path("img/dahuang3.bmp")]
    for i in arr:
        xy = find_cao_yao(hwnd, i)
        if None is not xy:
            print(f"find_da_huang_list 找到大黄={xy}")
            return xy
    return None


# find_qi_ma 是否在骑马
def find_qi_ma(hwnd, img_name):
    x_offset = int(w - 800)
    y_offset = 20

    xy = bg_find_pic_area.find_image_in_window(hwnd, img_name, x_offset, y_offset, w - 100, int(h * 0.3), 0.8)
    print(f"find_qi_ma xy = {xy}")
    if None is xy:
        return None

    x = scale * (int(xy[0]) + x_offset) + 15
    y = scale * (int(xy[1]) + y_offset) + 20
    print(f"find_qi_ma x={x}, y={y}")
    return x, y


def is_qi_ma(hwnd):
    arr = [win_tool.resource_path("img/qima_longma.bmp"), win_tool.resource_path("img/qima_yizhangxue.bmp"),
           win_tool.resource_path("img/qima_lianhuoliuli.bmp"), win_tool.resource_path("img/qima_moqiling.bmp")]
    for i in arr:
        xy = find_qi_ma(hwnd, i)
        time.sleep(0.2)
        if None is not xy:
            print(f"is_qi_ma 骑马了={i}")
            return True
    return False


# 如果没骑马就骑马
def qi_ma(hwnd):
    if not is_qi_ma(hwnd):
        print(f"{hwnd} 骑马")
        # win_tool.press('=')
        win_tool.send_key_to_window_frequency(hwnd, '=', 1)


# find_tu_dun 找土遁
def find_tu_dun(hwnd):
    x_offset = int(w * 0.1)
    y_offset = int(h * 0.4)
    tdxy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/tudun.bmp"), x_offset, y_offset, w,
                                                 h - 50, 0.8)
    print(f"hwnd = {hwnd} tdxy = {tdxy}")
    if None is tdxy:
        return None
    td_x = scale * (int(tdxy[0]) + x_offset) + 7
    td_y = scale * (int(tdxy[1]) + y_offset) + 10
    print(f"tdx={td_x}, tdy={td_y}")
    return td_x, td_y


# find_tu_dun_sui_mu 找土遁的碎木
def find_tu_dun_sui_mu(hwnd):
    x_offset = 300
    y_offset = 300

    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/suimusuoyaozhen.bmp"), x_offset,
                                               y_offset, int(w * 0.8), int(h * 0.8))
    print(f"find_tu_dun_sui_mu = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset) + 10
    y = scale * (int(xy[1]) + y_offset) + 10
    print(f"tdx={x}, tdy={y}")
    return x, y


# find_tu_dun_jiu_feng 找土遁的九凤
def find_tu_dun_jiu_feng(hwnd):
    x_offset = 300
    y_offset = 300

    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/tudun_jiufengling.bmp"), x_offset,
                                               y_offset, int(w * 0.8), int(h * 0.8))
    print(f"find_tu_dun_jiu_feng = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset) + 10
    y = scale * (int(xy[1]) + y_offset) + 10
    print(f"tdx={x}, tdy={y}")
    return x, y


def find_tu_dun_chu_fa(hwnd):
    x_offset = 300
    y_offset = 300
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/tudun_chufa.bmp"), x_offset, y_offset,
                                               int(w * 0.8), int(h * 0.8))
    print(f"find_tu_dun_chu_fa = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset) + 15
    y = scale * (int(xy[1]) + y_offset) + 15
    print(f"find_tu_dun_chu_fa={x}, tdy={y}")
    return x, y


def find_tu_dun_gou(hwnd):
    xy = find_pic(hwnd, win_tool.resource_path("img/tudun_gou.bmp"), int(w * 0.2), int(0.1*h), int(w * 0.7), int(h * 0.7), 0.8)
    print(f"find_tu_dun_gou = {xy}")
    if None is not xy:
        return xy[0], xy[1] + 12
    return None


def tu_dun_wa_dang(hwnd):
    res = ""
    for i in range(3):
        res = tu_dun_page1(hwnd, "img/tudun_wadang.bmp")
        if "" != res:
            time.sleep(6)
            continue
        else:
            break
    return res


def tu_dun_zhao_ge(hwnd):
    return tu_dun_page1(hwnd, "img/tudun_zhaoge.bmp")


def tu_dun_jin_lin(hwnd):
    return tu_dun_page1(hwnd, "img/tudun_jinlin.bmp")


def tu_dun_qion_yun(hwnd):
    return tu_dun_page1(hwnd, "img/tudun_qiongyundao.bmp")


def tu_dun_niao_shan(hwnd):
    return tu_dun_page1(hwnd, "img/tudun_niaoshan.bmp")


def tu_dun_page1(hwnd, img_name):
    try:
        okxy = find_tu_dun_gou(hwnd)
        if None is not okxy:
            win_tool.send_mouse_left_click(hwnd, okxy[0], okxy[1])
            time.sleep(0.5)
            return ""

        # 找到土遁
        tdxy = find_tu_dun(hwnd)
        if None is tdxy:
            return "未找到土遁！"
        td_x = tdxy[0]
        td_y = tdxy[1]
        log3.logger.info(f"tu_dun_page1 {img_name} {td_x} {td_y}")
        print(f"tdx={td_x}, tdy={td_y}")

        # 点击土遁
        # win_tool.send_input_mouse_left_click(td_x, td_y)
        win_tool.send_mouse_left_click(hwnd, td_x, td_y)
        time.sleep(0.5)

        # 找
        xy = find_pic(hwnd, img_name, int(w * 0.2), int(h * 0.1), int(w * 0.7), int(h * 0.7), 0.7)
        if None is xy:
            return f"未找到 {img_name}！"

        sm_x = xy[0]
        sm_y = xy[1]
        print(f"tdx={sm_x}, tdy={sm_y}")

        # 点击
        # win_tool.send_input_mouse_left_click(sm_x, sm_y)
        win_tool.send_mouse_left_click(hwnd, sm_x, sm_y)
        time.sleep(0.3)

        # 出发
        cfxy = find_tu_dun_chu_fa(hwnd)
        if None is cfxy:
            return "未找到出发！"

        cf_x = cfxy[0]
        cf_y = cfxy[1]
        print(f"tdx={cf_x}, tdy={cf_y}")
        # win_tool.send_input_mouse_left_click(cf_x, cf_y)
        win_tool.send_mouse_left_click(hwnd, cf_x, cf_y)
        time.sleep(0.5)

        # 确定
        for _ in range(3):
            okxy = find_tu_dun_gou(hwnd)
            if None is okxy:
                time.sleep(0.5)
                continue
            # win_tool.send_input_mouse_left_click(okxy[0], okxy[1])
            win_tool.send_mouse_left_click(hwnd,  okxy[0], okxy[1])
            time.sleep(0.3)
    except Exception as e:
        print(f"发生异常：{e} {traceback.format_exc()}")
        return traceback.format_exc()

    return ""


def tu_dun_sui_mu(hwnd):
    time.sleep(0.1)

    # 找到土遁
    tdxy = find_tu_dun(hwnd)
    if None is tdxy:
        return "未找到土遁！"
    td_x = tdxy[0]
    td_y = tdxy[1]
    print(f"tdx={td_x}, tdy={td_y}")

    # 点击土遁
    # win_tool.send_input_mouse_left_click(td_x, td_y)
    win_tool.send_mouse_left_click(hwnd, int(td_x), int(td_y))
    time.sleep(0.5)

    # 找碎木
    smxy = find_tu_dun_sui_mu(hwnd)
    if None is smxy:
        return "未找到碎木！"

    sm_x = smxy[0]
    sm_y = smxy[1]
    print(f"tdx={sm_x}, tdy={sm_y}")

    # 点击碎木锁妖阵
    # win_tool.send_input_mouse_left_click(sm_x, sm_y)
    win_tool.send_mouse_left_click(hwnd, int(sm_x), int(sm_y))
    time.sleep(0.3)

    # 出发
    cfxy = find_tu_dun_chu_fa(hwnd)
    if None is cfxy:
        return "未找到出发！"

    cf_x = cfxy[0]
    cf_y = cfxy[1]
    print(f"tdx={cf_x}, tdy={cf_y}")
    # win_tool.send_input_mouse_left_click(cf_x, cf_y)
    win_tool.send_mouse_left_click(hwnd, int(cf_x), int(cf_y))
    time.sleep(0.5)

    # 确定
    okxy = find_tu_dun_gou(hwnd)
    if None is okxy:
        return "未找到确定！"

    ok_x = okxy[0]
    ok_y = okxy[1]
    print(f"ok_x={ok_x}, ok_y={ok_y}")
    # win_tool.send_input_mouse_left_click(ok_x, ok_y)
    win_tool.send_mouse_left_click(hwnd, int(ok_x), int(ok_y))
    time.sleep(0.5)

    return ""


def tu_dun_jiu_feng(hwnd):
    time.sleep(0.1)

    # 找到土遁
    tdxy = find_tu_dun(hwnd)
    if None is tdxy:
        return "未找到土遁！"
    td_x = tdxy[0]
    td_y = tdxy[1]
    print(f"tdx={td_x}, tdy={td_y}")

    # 点击土遁
    win_tool.send_input_mouse_left_click(td_x, td_y)
    time.sleep(0.5)

    # 找九凤
    smxy = find_tu_dun_jiu_feng(hwnd)
    if None is smxy:
        return "未找到九凤！"

    sm_x = smxy[0]
    sm_y = smxy[1]
    print(f"tdx={sm_x}, tdy={sm_y}")

    # 点击
    win_tool.send_input_mouse_left_click(sm_x, sm_y)
    time.sleep(0.3)

    # 出发
    cfxy = find_tu_dun_chu_fa(hwnd)
    if None is cfxy:
        return "未找到出发！"

    cf_x = cfxy[0]
    cf_y = cfxy[1]
    print(f"tdx={cf_x}, tdy={cf_y}")
    win_tool.send_input_mouse_left_click(cf_x, cf_y)
    time.sleep(0.5)

    # 确定
    okxy = find_tu_dun_gou(hwnd)
    if None is okxy:
        return "未找到确定！"

    ok_x = okxy[0]
    ok_y = okxy[1]
    print(f"ok_x={ok_x}, ok_y={ok_y}")
    win_tool.send_input_mouse_left_click(ok_x, ok_y)
    time.sleep(0.5)

    return ""


def navigation_jian_tou(hwnd):
    x_offset = int(w / 2)
    y_offset = int(h / 2)
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/daohang_jiantou.bmp"), x_offset,
                                               y_offset, w - 50, h - 50)
    print(f"navigation_jian_tou = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset) + 5
    y = scale * (int(xy[1]) + y_offset) + 5
    print(f"navigation_jian_tou={x}, tdy={y}")
    return x, y


def navigation_shu_ru(hwnd):
    global navigation_shu_ru_x_y
    x_offset = int(w * 0.7)
    y_offset = int(h * 0.6)
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/daohang_shurukuan.bmp"), x_offset,
                                               y_offset, w, int(h * 0.9), 0.8)
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset) - 50
    y = scale * (int(xy[1]) + y_offset) + 15
    if None is navigation_shu_ru_x_y:
        navigation_shu_ru_x_y = [x, y]
    log3.logger.debug(f"navigation_shu_ru={x}, tdy={y}")
    return x, y


navigation_jian_tou_x_y = None
navigation_shu_ru_x_y = None


# open_navigation 打开导航，成功返回 输入框位置
def open_navigation(hwnd):
    global navigation_jian_tou_x_y
    global navigation_shu_ru_x_y
    # 每次打开导航前，检测是否有弹窗通知要关
    close_tong_zhi()

    sr_xy = navigation_shu_ru(hwnd)
    if None is not sr_xy:
        # 已经打开导航，找输入框 点击
        print(f"已经打开导航{sr_xy}")
        # win_tool.send_input_mouse_left_click(sr_xy[0], sr_xy[1])
        win_tool.send_mouse_left_click(hwnd, sr_xy[0], sr_xy[1])
        time.sleep(0.1)
        return sr_xy

    # 找箭头，点击：
    jt_xy = None
    if None is not navigation_jian_tou_x_y:
        jt_xy = navigation_jian_tou_x_y
    else:
        for i in range(3):
            jt_xy = navigation_jian_tou(hwnd)
            if None is jt_xy:
                time.sleep(0.1)
                continue
            else:
                break

        if None is jt_xy:
            time.sleep(0.1)
            close_tong_zhi()
            return "未找到导航箭头"
        navigation_jian_tou_x_y = jt_xy

    print(f"jt_x={jt_xy[0]}, jt_y={jt_xy[1]}")
    # win_tool.send_input_mouse_left_click(jt_xy[0], jt_xy[1])
    win_tool.send_mouse_left_click(hwnd, jt_xy[0], jt_xy[1])
    time.sleep(0.2)

    if None is not navigation_shu_ru_x_y:
        return navigation_shu_ru_x_y

    sr_xy = None
    for i in range(3):
        sr_xy = navigation_shu_ru(hwnd)
        if None is sr_xy:
            time.sleep(0.1)
            continue
        else:
            break

    if None is sr_xy:
        return "未找到导航输入框"
    return sr_xy


# 打开导航，并点击输入框，主要用途是后台操作鼠标时重置有悬停特效的鼠标焦点
def open_navigation_and_click(hwnd):
    # 打开导航
    on_xy = open_navigation(hwnd)
    if isinstance(on_xy, str):
        return on_xy
    win_tool.move_mouse_to(hwnd, on_xy[0], on_xy[1])
    time.sleep(0.01)
    win_tool.send_mouse_left_click(hwnd, on_xy[0], on_xy[1])
    time.sleep(0.01)
    win_tool.send_key_to_window_frequency(hwnd, "esc")


# navigation_x_y 导航去指定坐标
def navigation_x_y(hwnd, xy):
    # 打开导航
    on_xy = open_navigation(hwnd)
    if isinstance(on_xy, str):
        return on_xy

    # win_tool.move_mouse(on_xy[0], on_xy[1])
    # time.sleep(0.1)
    # win_tool.mouse_left_click()
    # time.sleep(0.1)
    win_tool.send_mouse_left_click(hwnd, on_xy[0], on_xy[1])
    # win_tool.press_backspace(20)
    win_tool.send_key_to_window_backspace(hwnd, 20)

    time.sleep(0.1)
    win_tool.send_text_to_hwnd(hwnd, xy)
    time.sleep(0.3)
    win_tool.send_key_to_window_enter(hwnd)

    # time.sleep(0.1)
    # win_tool.paste_text(xy)
    # time.sleep(0.05)
    # win_tool.press_enter()
    # time.sleep(0.1)
    return on_xy


# 根据导航的图 来找
def navigation_name(hwnd, name):
    # 打开导航
    on_xy = open_navigation(hwnd)
    if isinstance(on_xy, str):
        return on_xy

    # 鼠标移动到导航的上面，可以操作鼠标滚轮
    # win_tool.move_mouse(on_xy[0] - 50, on_xy[1] - 100)
    # time.sleep(0.25)

    # 鼠标往上，把导航置顶
    for i in range(12):
        # win_tool.scroll_mouse_up(600)
        # time.sleep(0.04)
        win_tool.scroll_mouse_wheel_at(hwnd, on_xy[0] - 50, on_xy[1] - 100, 600)
        time.sleep(0.04)

    for _ in range(25):
        # 识图，找
        time.sleep(0.35)
        xy = find_pic(hwnd, name, int(w * 0.7), int(h * 0.5), w, int(h * 0.95))
        if None is xy:
            print(f"没找到 {name}")
            # 鼠标往下滚
            # win_tool.scroll_mouse_down(240)
            win_tool.scroll_mouse_wheel_at(hwnd, on_xy[0] - 50, on_xy[1] - 100, -240)
            continue
        # win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
        win_tool.send_mouse_left_click(hwnd, xy[0] + 5, xy[1] + 5)
        time.sleep(0.15)
        return xy

    return f"未找到 {name}"


# 相机抬最高
def camera_top(hwnd):
    win_tool.SendMessageW_Extended_KEY(hwnd, win_tool.VK_NUMPAD5)
    time.sleep(0.05)
    win_tool.SendMessageW_Extended_KEY(hwnd, win_tool.VK_NUMPAD2, 0.5)
    time.sleep(0.05)
    win_tool.scroll_mouse_wheel_at(hwnd, 500, 500, -120)
    time.sleep(0.05)


# 相机抬摆正
def camera_forward(hwnd):
    win_tool.SendMessageW_Extended_KEY(hwnd, win_tool.VK_NUMPAD5)
    time.sleep(0.05)
    win_tool.scroll_mouse_wheel_at(hwnd, 500, 500, -120)
    win_tool.scroll_mouse_wheel_at(hwnd, 500, 500, -120)


def camera_left(hwnd):
    win_tool.SendMessageW_Extended_KEY(hwnd, win_tool.VK_NUMPAD4, 0.1)


def camera_right(hwnd):
    win_tool.SendMessageW_Extended_KEY(hwnd, win_tool.VK_NUMPAD6, 0.1)


# 说话
def say(text, hwnd=None):
    print(text)
    text = f"{app_const.APP_VERSION}：{text}"
    log3.logger.info(text)
    if None is hwnd:
        win_tool.press_enter()
        win_tool.paste_text(text)
        win_tool.press_enter()
        time.sleep(0.02)

    if None is not hwnd and win_tool.is_window_foreground(hwnd):
        win_tool.press_enter()
        win_tool.paste_text(text)
        win_tool.press_enter()
        time.sleep(0.02)


def say_hwnd(hwnd, text):
    text = f"{app_const.APP_VERSION}：{text}"
    log3.logger.info(f"{hwnd} - {text}")
    if not win32gui.IsWindow(hwnd):
        return None
    with lock:
        # time.sleep(0.01)
        win_tool.send_key_to_window_enter(hwnd)
        time.sleep(0.01)
        win_tool.send_text_to_hwnd(hwnd, text)
        time.sleep(0.01)
        win_tool.send_key_to_window_enter(hwnd)
        time.sleep(0.05)


# 关闭刀剑2 通知
def close_tong_zhi():
    with lock:
        try:
            d_h = win_tool.get_desktop_window_handle()
            xy = find_pic_original(d_h, "img/daojian2tongzhi_close.bmp", int(w * 0.9), int(h * 0.6), w, h - 50, 0.9, True)
            if None is xy:
                return
            print(f"关闭通知{xy}")
            say("别号有弹窗通知，关闭。")
            # win_tool.send_input_mouse_left_click(xy[0] + 8, xy[1] + 13)
            win_tool.send_mouse_left_click(d_h, xy[0] + 8, xy[1] + 13)
            time.sleep(0.1)
        except Exception as e:
            print(f"发生异常：{e} {traceback.format_exc()}")
            return


# open_bag 打开背包，一打开不会重复打开
def open_bag(hwnd):
    # 找到背包的位置
    xy = find_pic(hwnd, "img/dakai_debeibao.bmp", 400, 0, w - 200, int(h * 0.6))
    if None is xy:
        # 背包没打开,按B
        # win_tool.send_key("b", 1)
        win_tool.send_key_to_window_frequency(hwnd, "b")
        time.sleep(0.1)
        return


# close_bag 关闭背包
def close_bag(hwnd):
    # 找到背包的位置
    xy = find_pic(hwnd, "img/dakai_debeibao.bmp", 400, 0, w - 200, int(h * 0.6))
    if None is xy:
        return
    # 背包打开,按B 关闭
    win_tool.send_key("b", 1)
    time.sleep(0.1)


# 打开装备
def open_zhuangbei(hwnd):
    # xy = find_pic(hwnd, "img/zhuangbei.bmp", int(0.1 * w), 0, int(w * 0.8), int(h * 0.5), 0.8)
    xy = find_pic(hwnd, "img/zhuangbei_guaxiang.bmp", 10, int(0.2 * h), int(w * 0.9), int(h * 0.9), 0.8)
    if None is xy:
        # 按 c
        win_tool.send_key_to_window_frequency(hwnd, "c")
        time.sleep(0.1)


def close_zhuangbei(hwnd):
    xy = find_pic(hwnd, "img/zhuangbei_guaxiang.bmp", 10, int(0.2 * h), int(w * 0.9), int(h * 0.9), 0.8)
    # xy = find_pic(hwnd, "img/zhuangbei.bmp", int(0.1 * w), 0, int(w * 0.8), int(h * 0.5), 0.8)
    if None is not xy:
        win_tool.send_key_to_window_frequency(hwnd, "c")
        time.sleep(0.1)


# 关闭 6 点的弹窗
def close_6_oclock_dialog(hwnd):
    xy = find_pic(hwnd, "img/6oclock_dialog_close.bmp", int(w * 0.4), 50, w - 150, int(h * 0.5), 0.8)
    if None is not xy:
        # win_tool.send_input_mouse_left_click(xy[0]+13, xy[1] + 13)
        win_tool.send_mouse_left_click(hwnd, xy[0] + 13, xy[1] + 13)
        time.sleep(0.1)
    xy = find_pic(hwnd, "img/xuanyuan_close_btn.bmp", int(w * 0.4), int(h * 0.3), int(w * 0.8), int(h * 0.5), 0.8)
    if None is not xy:
        # win_tool.send_input_mouse_left_click(xy[0]+13, xy[1] + 13)
        win_tool.send_mouse_left_click(hwnd, xy[0] + 13, xy[1] + 13)
        time.sleep(0.1)


# 用于重置某些对话状态，按一下ESC，如果是对话状态会退出，如果弹出设置会自动点返回游戏
def esc_and_back(hwnd):
    # 按一下 ESC， escfanhuiyouxi
    win_tool.send_key_to_window_frequency(hwnd, "esc", 1)
    time.sleep(0.5)
    xy = find_pic(hwnd, "img/escfanhuiyouxi.bmp", int(0.2 * w), int(0.1 * h), int(w * 0.8), int(h * 0.9),
                              0.75)
    if None is not xy:
        win_tool.activate_window(hwnd)
        time.sleep(0.1)
        # win_tool.send_input_mouse_left_click(xy[0]+5, xy[1]+5)
        win_tool.send_mouse_left_click(hwnd, xy[0] + 5, xy[1] + 5)
    return xy


# 是否在战斗状态
def is_battle(hwnd):
    xy = find_pic(hwnd, "img/zhandouzhuangtai.bmp", int(0.2 * w), int(0.7 * h), int(w * 0.8), h-30,0.8)
    if None is xy:
        return False
    log3.logger.info(f"战斗状态检测 is_battle {xy}")
    return True


# 防止暂离
def activity_window(hwnd=None):
    win_tool.send_key("f8")


# 挖草
def wa_cao(hwnd, xy):
    if win_tool.is_window_foreground(hwnd):
        win_tool.send_mouse_left_click(hwnd, xy[0]+4, xy[1]+8)
        time.sleep(5.7)
        return
    for _ in range(3):
        time.sleep(0.05)
        open_navigation_and_click(hwnd)
        time.sleep(0.05)
        win_tool.move_mouse_to(hwnd, xy[0]+4, xy[1]+8)
        time.sleep(0.05)
        win_tool.send_mouse_left_click(hwnd, xy[0]+4, xy[1]+8)
        time.sleep(0.06)
        win_tool.send_mouse_left_click(hwnd, xy[0]+4, xy[1]+8)
        time.sleep(5.7)


if __name__ == "__main__":
    pass
    # time.sleep(3)
    # window_name = "夏禹剑 - 刀剑2"
    # hwnd = win_tool.get_window_handle(window_name)
    # print(is_battle(hwnd))
