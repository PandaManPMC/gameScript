
import time
import win_tool
import bg_find_pic_area
import threading
from tkinter import messagebox
import win32con
import win32api
import app_const
import traceback

scale = win_tool.get_screen_scale()
w, h = win_tool.get_win_w_h()


def find_pic_original(hwnd, img_name, x_offset, y_offset, width, height, threshold=0.7):
    print(f"find_pic_original hwnd={hwnd} img_name={img_name} x_offset={x_offset}, y_offset={y_offset}, w={width}, h={int(height)}")
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path(img_name), x_offset, y_offset, width, height, threshold)
    print(f"find_pic_original xy = {xy}")
    if None is xy:
        return None
    x = int(xy[0] + x_offset)
    y = int(xy[1] + y_offset)
    print(f"find_pic_original x={x}, y={y}")
    return x, y


def find_pic(hwnd, img_name, x_offset, y_offset, width, height, threshold=0.7):
    print(f"find_pic hwnd={hwnd} img_name={img_name} x_offset={x_offset}, y_offset={y_offset}, w={width}, h={int(height)}")
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path(img_name), x_offset, y_offset, width, height, threshold)
    print(f"find_pic xy = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset)
    y = scale * (int(xy[1]) + y_offset)
    print(f"find_pic x={x}, y={y}")
    return x, y


# 是否死亡
def is_die(hwnd):
    xy = find_pic(hwnd, "img/huangquanzhilu.bmp", 300, 300, int(w * 0.7), int(h * 0.6))
    if None is xy:
        print(f"{hwnd}-检测死亡状态-未死亡")
        return None
    print(f"{hwnd}-检测死亡状态-已死亡")
    return xy


# 是否死亡（复活点）
def is_die_dian(hwnd):
    xy = find_pic(hwnd, "img/fuhuodianfuhuo.bmp", 300, 300, int(w * 0.7), int(h * 0.6))
    if None is xy:
        print(f"{hwnd}-检测死亡状态-未死亡")
        return None
    print(f"{hwnd}-检测死亡状态-已死亡")
    return xy


def find_lvse_shouzhang(hwnd):
    x_offset = 500
    y_offset = int(h * 0.2)
    print(f"find_lvse_shouzhang x_offset={x_offset}, y_offset={y_offset}, w={int(w*0.7)}, h={int(h*0.8)}")
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/lvse_shouzhang.bmp"), x_offset, y_offset, int(w*0.7), int(h*0.7))
    print(f"find_lvse_shouzhang xy = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset)
    y = scale * (int(xy[1]) + y_offset)
    print(f"find_lvse_shouzhang x={x}, y={y}")
    return x, y


# find_cao_yao 找草药
def find_cao_yao(hwnd, img_name):
    x_offset = 500
    y_offset = int(h * 0.2)
    print(f"find_da_huang x_offset={x_offset}, y_offset={y_offset}, w={int(w*0.5)}, h={int(h*0.8)}")
    xy = bg_find_pic_area.find_image_in_window(hwnd, img_name, x_offset, y_offset, int(w*0.5), int(h*0.7))
    print(f"find_da_huang xy = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset) + 10
    y = scale * (int(xy[1]) + y_offset) + 35
    print(f"find_da_huang x={x}, y={y}")
    return x, y


def find_gan_cao_list(hwnd):
    arr = [win_tool.resource_path("img/gancao1.bmp"), win_tool.resource_path("img/gancao2.bmp"), win_tool.resource_path("img/gancao3.bmp"), win_tool.resource_path("img/gancao4.bmp")]
    for i in arr:
        xy = find_cao_yao(hwnd, i)
        if None is not xy:
            print(f"find_gan_cao_list 找到甘草={xy}")
            return xy
    return None


def find_da_huang_list(hwnd):
    arr = [win_tool.resource_path("img/dahuang.bmp"), win_tool.resource_path("img/dahuang2.bmp"), win_tool.resource_path("img/dahuang3.bmp")]
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
    arr = [win_tool.resource_path("img/qima_longma.bmp"), win_tool.resource_path("img/qima_yizhangxue.bmp"), win_tool.resource_path("img/qima_lianhuoliuli.bmp"), win_tool.resource_path("img/qima_moqiling.bmp")]
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
        win_tool.press('=')


# find_tu_dun 找土遁
def find_tu_dun(hwnd):
    x_offset = 300
    y_offset = int(h / 2)
    tdxy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/tudun.bmp"), x_offset, y_offset, w, h)
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

    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/suimusuoyaozhen.bmp"), x_offset, y_offset, int(w * 0.8), int(h * 0.8))
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

    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/tudun_jiufengling.bmp"), x_offset, y_offset, int(w * 0.8), int(h * 0.8))
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
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/tudun_chufa.bmp"), x_offset, y_offset, int(w * 0.8), int(h * 0.8))
    print(f"find_tu_dun_chu_fa = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset) + 15
    y = scale * (int(xy[1]) + y_offset) + 15
    print(f"find_tu_dun_chu_fa={x}, tdy={y}")
    return x, y


def find_tu_dun_gou(hwnd):
    xy = find_pic(hwnd, win_tool.resource_path("img/tudun_gou.bmp"), 300, 300, int(w * 0.6), int(h * 0.6), 0.8)
    print(f"find_tu_dun_gou = {xy}")
    if None is xy:
        return None
    return xy[0], xy[1] + 12


def tu_dun_wa_dang(hwnd):
    return tu_dun_page1(hwnd, "img/tudun_wadang.bmp")


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

        # 找瓦当
        xy = find_pic(hwnd, img_name, 400, 200, int(w * 0.6), int(h * 0.6))
        if None is xy:
            return "未找到 tudun_wadang.bmp！"

        sm_x = xy[0]
        sm_y = xy[1]
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
    win_tool.send_input_mouse_left_click(td_x, td_y)
    time.sleep(0.5)

    # 找碎木
    smxy = find_tu_dun_sui_mu(hwnd)
    if None is smxy:
        return "未找到碎木！"

    sm_x = smxy[0]
    sm_y = smxy[1]
    print(f"tdx={sm_x}, tdy={sm_y}")

    # 点击碎木锁妖阵
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
    x_offset = int(w/2)
    y_offset = int(h/2)
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/daohang_jiantou.bmp"), x_offset, y_offset, w-50, h-50)
    print(f"navigation_jian_tou = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset) + 5
    y = scale * (int(xy[1]) + y_offset) + 5
    print(f"navigation_jian_tou={x}, tdy={y}")
    return x, y


def navigation_shu_ru(hwnd):
    x_offset = int(w/2)
    y_offset = int(h/2)
    xy = bg_find_pic_area.find_image_in_window(hwnd, win_tool.resource_path("img/daohang_shurukuan.bmp"), x_offset, y_offset, w, h-50)
    print(f"navigation_shu_ru = {xy}")
    if None is xy:
        return None
    x = scale * (int(xy[0]) + x_offset) - 50
    y = scale * (int(xy[1]) + y_offset) + 15
    print(f"navigation_shu_ru={x}, tdy={y}")
    return x, y


# open_navigation 打开导航，成功返回 输入框位置
def open_navigation(hwnd):
    # 每次打开导航前，检测是否有弹窗通知要关
    close_tong_zhi()

    sr_xy = navigation_shu_ru(hwnd)
    if None is not sr_xy:
        # 已经打开导航，找输入框 点击
        print(f"已经打开导航{sr_xy}")
        win_tool.send_input_mouse_left_click(sr_xy[0], sr_xy[1])
        time.sleep(0.1)
        return sr_xy

    # 找箭头，点击
    jt_xy = navigation_jian_tou(hwnd)
    if None is jt_xy:
        return "未找到导航箭头"

    print(f"jt_x={jt_xy[0]}, jt_y={jt_xy[1]}")
    win_tool.send_input_mouse_left_click(jt_xy[0], jt_xy[1])
    time.sleep(0.2)

    sr_xy = navigation_shu_ru(hwnd)
    if None is sr_xy:
        return "未找到导航输入框"

    return sr_xy


# navigation_x_y 导航去指定坐标
def navigation_x_y(hwnd, xy):
    # 打开导航
    on_xy = open_navigation(hwnd)
    if isinstance(on_xy, str):
        return on_xy

    win_tool.move_mouse(on_xy[0], on_xy[1])
    time.sleep(0.1)
    win_tool.mouse_left_click()
    time.sleep(0.1)
    win_tool.press_backspace(20)
    time.sleep(0.1)
    win_tool.paste_text(xy)
    time.sleep(0.05)
    win_tool.press_enter()
    time.sleep(0.1)


# 根据导航的图 来找
def navigation_name(hwnd, name):
    # 打开导航
    on_xy = open_navigation(hwnd)
    if isinstance(on_xy, str):
        return on_xy

    # 鼠标移动到导航的上面，可以操作鼠标滚轮
    win_tool.move_mouse(on_xy[0] - 50, on_xy[1] - 100)
    time.sleep(0.1)

    for i in range(25):
        # 鼠标往下滚
        win_tool.scroll_mouse_down(240)
        time.sleep(0.25)

        # 识图，找
        xy = find_pic(hwnd, name, 1000, 500, w, h)
        if None is xy:
            print(f"没找到 {name}")
            continue
        win_tool.send_input_mouse_left_click(xy[0] + 5, xy[1] + 5)
        time.sleep(0.1)
        return xy

    return f"未找到 {name}"


# 相机抬最高
def camera_top():
    win32api.keybd_event(win32con.VK_NUMPAD5, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(win32con.VK_NUMPAD5, 0, win32con.KEYEVENTF_KEYUP, 0)

    time.sleep(0.1)
    win32api.keybd_event(win32con.VK_NUMPAD2, 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(win32con.VK_NUMPAD2, 0, win32con.KEYEVENTF_KEYUP, 0)

    win_tool.scroll_mouse_down(120)
    time.sleep(0.3)


# 相机抬摆正
def camera_forward():
    win32api.keybd_event(win32con.VK_NUMPAD5, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(win32con.VK_NUMPAD5, 0, win32con.KEYEVENTF_KEYUP, 0)

    win_tool.scroll_mouse_down(120)
    time.sleep(0.3)


# 说话
def say(text):
    print(text)
    text = f"{app_const.APP_NAME}：{text}"
    win_tool.press_enter()
    win_tool.paste_text(text)
    win_tool.press_enter()
    time.sleep(0.02)


# 关闭刀剑2 通知
def close_tong_zhi():
    try:
        d_h = win_tool.get_desktop_window_handle()
        xy = find_pic_original(d_h, "img/daojian2tongzhi_close.bmp", int(w * 0.7), int(h * 0.6), w, h, 0.8)
        if None is xy:
            return
        print(f"关闭通知{xy}")
        say("别号有弹窗通知，关闭。")
        win_tool.send_input_mouse_left_click(xy[0] + 8, xy[1] + 13)
        time.sleep(0.1)
    except Exception as e:
        print(f"发生异常：{e} {traceback.format_exc()}")
        return


# open_bag 打开背包，一打开不会重复打开
def open_bag(hwnd):
    # 找到背包的位置
    xy = find_pic(hwnd, "img/dakai_debeibao.bmp", 400, 0, w-200, int(h * 0.6))
    if None is xy:
        # 背包没打开,按B
        win_tool.send_key("b", 1)
        time.sleep(0.1)
        return


# close_bag 关闭背包
def close_bag(hwnd):
    # 找到背包的位置
    xy = find_pic(hwnd, "img/dakai_debeibao.bmp", 400, 0, w-200, int(h * 0.6))
    if None is xy:
        return
    # 背包打开,按B 关闭
    win_tool.send_key("b", 1)
    time.sleep(0.1)


# 打开背包
def open_zhuangbei(hwnd):
    xy2 = find_pic(hwnd, "img/zhuangbei.bmp", 300, 0, w - 20, int(h * 0.5), 0.8)
    if None is xy2:
        # 按 B 打开背包
        win_tool.send_key("c")
        time.sleep(0.1)


def close_zhuangbei(hwnd):
    xy2 = find_pic(hwnd, "img/zhuangbei.bmp", 300, 0, w - 20, int(h * 0.5), 0.8)
    if None is not xy2:
        # 按 B 打开背包
        win_tool.send_key("c")
        time.sleep(0.1)


# 关闭 6 点的弹窗
def close_6_oclock_dialog(hwnd):
    xy = find_pic(hwnd, "img/6oclock_dialog_close.bmp", 300, 50, w - 200, int(h * 0.5))
    if None is xy:
        return
    win_tool.send_input_mouse_left_click(xy[0]+13, xy[1] + 13)
    time.sleep(0.1)



if __name__ == "__main__":
    # time.sleep(3)
    window_name = "夏禹剑 - 刀剑2"
    hwnd = win_tool.get_window_handle(window_name)

    # hwnd = desktop_handle = win_tool.get_desktop_window_handle()
    # xy = find_pic_original(hwnd, "img/daojian2tongzhi_close.bmp", int(w*0.75), int(h*0.6), w, h)

    # xy = find_pic(hwnd, "img/beibao_zhuangguwang.bmp", 500, 500, w-400, int(h * 0.9), 0.9)
    # xy = find_pic(hwnd, "img/tudun_niaoshan.bmp", 500, 200, w-400, int(h * 0.9))
    # xy = find_pic(hwnd, "img/jiufeng_jiaogeiwoba.bmp", 0, 100, w-400, int(h * 0.9))
    # xy = find_pic(hwnd, "img/niaoshan_zhoumosishi.bmp", 500, 200, w - 400, int(h * 0.9))
    # xy = find_pic(hwnd, "img/qiongyun_luwushuang_touxiang.bmp", 500, 0, w - 500, int(h * 0.3))
    # xy = find_pic(hwnd, "img/beibao_wutianling.bmp", 0, 0, w, int(h * 0.5), 0.8)
    # xy = find_pic(hwnd, "img/muye_daocaoren.bmp", 300, 0, w - 20, int(h * 0.3))

    # xy = find_pic(hwnd, "img/zhuangbei.bmp", 300, 0, w - 20, int(h * 0.5))
    # xy = find_pic(hwnd, "img/6oclock_dialog_close.bmp", 300, 50, w - 200, int(h * 0.5))

    # x_offset = 500
    # y_offset = int(h * 0.2)

    time.sleep(2)
    xy = find_pic(hwnd, "img/fuwuqi_chengzhangdengji_40.bmp", 50, 0, w - 20, int(h * 0.4))
    # xy = find_pic(hwnd, "img/fuwuqi_chengzhangdengji_20.bmp", 50, 0, w - 20, int(h * 0.4), 0.8)

    print(f"xy={xy}")
    if None is not xy:
        win_tool.move_mouse(xy[0]+13, xy[1] + 13)
        time.sleep(0.2)
        # win_tool.mouse_left_click()

    # while True:
    #     time.sleep(0.3)
    #     xy = find_pic(hwnd, "img/niaoshan_geyucheng.bmp", 500, 100, int(w * 0.8), int(h * 0.5))
    #     if None is not xy:
    #         win_tool.move_mouse(xy[0], xy[1])
    #         break
    '''
    time.sleep(3)
    while True:
        print("scroll_mouse_down")
        win_tool.scroll_mouse_down(120)
        time.sleep(0.5)
    '''