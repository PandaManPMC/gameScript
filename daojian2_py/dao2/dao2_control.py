import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import keyboard
from tkinter import messagebox

import win_tool
import dao2_wa_dahuang
import dao2_wa_gancao
import i_mouse
import dao2_everyday
import dao2_gu_cheng
import dao2_quick
import app_const
import dao2_da_qunxia
import dao2_muye_fuwuqi
import dao2_gu_cheng_treasure
import log3
import dao2_arena
import app
import dao2_wa_ma_huang
import dao2_wa_baishu
import dao2_common
import dao2_equipage
import dao2_six_contest
import dao2_wa_wuweicao
import dao2_wa_danghuang
import dao2_wa_chaihu
import dao2_wa_chuanqiong
import dao2_wa_jinxianlian
import dao2_wa_banxia
import dao2_wa_niu_jin_cao
import dao2_wa_xi_hun_kuangshi

#window_name = "夏禹剑 - 刀剑2"
window_name = "刀剑2"

# 全局变量用于控制“一直按键”子线程
keep_pressing = False

# 窗口置顶
topmost = False

# 窗口句柄
hwnd_array = []

hwnd_array_str = []

# 全局UI控制锁
LOCK_GLOBAL_UI = threading.Lock()


def root_click(event):
    # 在点击其他地方时，将焦点移出输入框
    # input_entry.focus_out()
    # num_entry.focus_out()
    # input_hwnd_send_key.focus_out()
    # mu_ye_entry.focus_out()
    if event.widget != input_entry \
            and event.widget != input_entry \
            and event.widget != input_hwnd_send_key \
            and event.widget != mu_ye_entry \
            and event.widget != input_say_time \
            and event.widget != input_say_content:  # 只有点击其他地方才失去焦点

        root.focus_set()


def toggle_collect(event=None):
    log3.console(f"触发 toggle_collect")
    if event is not None and event.type != '2':  # 2表示 KeyPress 事件
        return

    with dao2_quick.lockCollect:
        dao2_quick.runningCollect = not dao2_quick.runningCollect
        if dao2_quick.runningCollect:
            btn_collect.config(bg="red")
            t = threading.Thread(target=dao2_quick.collect, args=(window_name,), daemon=True)
            t.start()
        else:
            btn_collect.config(bg="white")


def mount_all(event=None):
    log3.console("触发全体上马")
    global window_name
    win_tool.send_key_to_all_windows(window_name, 0xBB)


def receive_notify(event=None):
    log3.console("receive_notify 接通知")
    with LOCK_GLOBAL_UI:
        dao2_quick.is_run_receive_notify = not dao2_quick.is_run_receive_notify
        log3.console(f"receive_notify {dao2_quick.is_run_receive_notify}")

    with dao2_quick.lock:
        if dao2_quick.is_run_receive_notify:
            btn_receive_notify.config(bg="red")
            t = threading.Thread(target=dao2_quick.receive_notify(hwnd_array), args=(hwnd_array,), daemon=True)
            t.start()
        else:
            btn_receive_notify.config(bg="white")


def auto_team(event=None):
    log3.console("自动组队")
    with LOCK_GLOBAL_UI:
        dao2_quick.is_auto_team = not dao2_quick.is_auto_team
        log3.console(f"auto_team {dao2_quick.is_auto_team}")

    with dao2_quick.lock:
        if dao2_quick.is_auto_team:
            btn_auto_team.config(bg="red")
            t = threading.Thread(target=dao2_quick.auto_team(hwnd_array), args=(hwnd_array,), daemon=True)
            t.start()
        else:
            btn_auto_team.config(bg="white")


def mouse_right_click(event=None):
    with LOCK_GLOBAL_UI:
        i_mouse.is_run_mouse_right_click = not i_mouse.is_run_mouse_right_click
        log3.console(f"鼠标右键点击{i_mouse.is_run_mouse_right_click}")

    interval = 0.05
    with i_mouse.lock_run_mouse_right_click:
        if i_mouse.is_run_mouse_right_click:
            btn_mouse_right_click.config(bg="red")
            t = threading.Thread(target=i_mouse.while_mouse_right_click, args=(interval,), daemon=True)
            t.start()
        else:
            btn_mouse_right_click.config(bg="white")


def mouse_left_click(event=None):
    with LOCK_GLOBAL_UI:
        i_mouse.is_run_mouse_left_click = not i_mouse.is_run_mouse_left_click
        log3.console(f"鼠标左键点击{i_mouse.is_run_mouse_left_click}")
    interval = 0.05
    with i_mouse.lock_run_mouse_left_click:
        if i_mouse.is_run_mouse_left_click:
            btn_mouse_left_click.config(bg="red")
            t = threading.Thread(target=i_mouse.while_mouse_left_click, args=(interval,), daemon=True)
            t.start()
        else:
            btn_mouse_left_click.config(bg="white")


def say_switch(event=None):
    with LOCK_GLOBAL_UI:
        dao2_common.is_open_say = not dao2_common.is_open_say
        if dao2_common.is_open_say:
            btn_say_switch.config(bg="white")
        else:
            btn_say_switch.config(bg="red")


def toggle_topmost():
    global topmost
    topmost = not topmost
    if topmost:
        root.attributes('-topmost', True)
        btn_topmost.config(text="取消置顶")
        log3.console("窗口已置顶")
    else:
        root.attributes('-topmost', False)
        btn_topmost.config(text="窗口置顶")
        log3.console("取消窗口置顶")


def send_input_key():
    input_value = input_entry.get().strip().lower()
    if not input_value:
        log3.console("输入框为空")
        return

    key_code = win_tool.key_map.get(input_value)
    if key_code:
        log3.console(f"输入的内容：{input_value}，对应的按键码：{key_code}")
        win_tool.send_key_to_all_windows(window_name, key_code)
    else:
        log3.console(f"未找到对应的按键码：{input_value}")


def keep_sending_key():
    global keep_pressing
    keep_pressing = not keep_pressing

    if keep_pressing:
        btn_keep_pressing.config(text="停止按键")
        key_to_send = input_entry.get().strip().lower()
        num_input = num_entry.get().strip()

        if not key_to_send or not num_input:
            log3.console("按键或时间间隔输入无效")
            keep_pressing = False
            btn_keep_pressing.config(text="一直按键")
            return

        key_code = win_tool.key_map.get(key_to_send)
        interval = float(num_input)

        if key_code:
            log3.console(f"开始不断发送按键：{key_code}，间隔：{interval} 秒")
            t = threading.Thread(target=send_key_continuously, args=(key_code, interval), daemon=True)
            t.start()
        else:
            log3.console(f"未找到按键码：{key_to_send}")
            keep_pressing = False
            btn_keep_pressing.config(text="一直按键")
    else:
        btn_keep_pressing.config(text="一直按键")
        log3.console("停止发送按键")


def send_key_by_hwnd():
    selected_index = combobox.current()  # 获取选择框的当前下标
    log3.console(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]
    key_to_send = input_hwnd_send_key.get().strip().lower()
    delay = mu_ye_entry.get().strip()
    log3.console(f"指定hwnd={hwnd}一直按键{key_to_send},延迟={delay}")

    with LOCK_GLOBAL_UI:
        dao2_quick.is_run_send_key_by_hwnd = not dao2_quick.is_run_send_key_by_hwnd
        if dao2_quick.is_run_send_key_by_hwnd:
            btn_hwnd_send_key.config(bg="red")
            t = threading.Thread(target=dao2_quick.send_key_by_hwnd, args=(hwnd, key_to_send, delay,), daemon=True)
            t.start()
        else:
            btn_hwnd_send_key.config(bg="white")


def my_fuwuqi():
    log3.console("my_fuwuqi")
    with LOCK_GLOBAL_UI:
        dao2_muye_fuwuqi.is_run = not dao2_muye_fuwuqi.is_run
        log3.console(f"dao2_muye_fuwuqi {dao2_muye_fuwuqi.is_run}")

    with dao2_muye_fuwuqi.lock:
        selected_index = combobox.current()  # 获取选择框的当前下标
        log3.console(f"选择的下标：{selected_index}")
        hwnd = hwnd_array[selected_index]
        delay = mu_ye_entry.get().strip()

        if dao2_muye_fuwuqi.is_run:
            btn_mu_ye.config(bg="red")
            t = threading.Thread(target=dao2_muye_fuwuqi.start_mu_ye, args=(hwnd, delay,), daemon=True)
            t.start()
        else:
            btn_mu_ye.config(bg="white")


def qiang_hua():
    log3.console("qiang_hua")
    with LOCK_GLOBAL_UI:
        dao2_equipage.is_run_qiang_hua = not dao2_equipage.is_run_qiang_hua
        log3.console(f"dao2_equipage.is_run_qiang_hua {dao2_equipage.is_run_qiang_hua}")
        selected_index = combobox.current()
        log3.console(f"选择的下标：{selected_index}")
        hwnd = hwnd_array[selected_index]

        if dao2_equipage.is_run_qiang_hua:
            btn_qiang_hua.config(bg="red")
            t = threading.Thread(target=dao2_equipage.run_qiang_hua, args=(hwnd,), daemon=True)
            t.start()
        else:
            btn_qiang_hua.config(bg="white")


def ren_zhu():
    log3.console("ren_zhu")
    with LOCK_GLOBAL_UI:
        dao2_equipage.is_run_ren_zhu = not dao2_equipage.is_run_ren_zhu
        log3.console(f"dao2_equipage.is_run_ren_zhu {dao2_equipage.is_run_ren_zhu}")
        selected_index = combobox.current()
        log3.console(f"选择的下标：{selected_index}")
        hwnd = hwnd_array[selected_index]

        if dao2_equipage.is_run_ren_zhu:
            btn_ren_zhu.config(bg="red")
            t = threading.Thread(target=dao2_equipage.run_ren_zhu, args=(hwnd,), daemon=True)
            t.start()
        else:
            btn_ren_zhu.config(bg="white")


def saying():
    selected_index = combobox.current()  # 获取选择框的当前下标
    hwnd = hwnd_array[selected_index]

    content = input_say_content.get().strip()
    delay = input_say_time.get().strip()
    log3.console(f"指定hwnd={hwnd} 延迟={delay} 发言 {content}")

    with LOCK_GLOBAL_UI:
        dao2_quick.is_run_auto_say = not dao2_quick.is_run_auto_say
        if dao2_quick.is_run_auto_say:
            btn_start_say.config(bg="red")
            t = threading.Thread(target=dao2_quick.auto_say, args=(hwnd, delay, content,), daemon=True)
            t.start()
        else:
            btn_start_say.config(bg="white")


def six_contest():
    with LOCK_GLOBAL_UI:
        dao2_six_contest.is_run = not dao2_six_contest.is_run
        log3.console(f"dao2_six_contest.is_run {dao2_six_contest.is_run}")
        selected_index = combobox.current()
        log3.console(f"选择的下标：{selected_index}")
        hwnd = hwnd_array[selected_index]

        if dao2_six_contest.is_run:
            btn_six_contest.config(bg="red")
            t = threading.Thread(target=dao2_six_contest.run_six_contest, args=(hwnd,), daemon=True)
            t.start()
        else:
            btn_six_contest.config(bg="white")


def send_key_continuously(key_code, interval):
    global keep_pressing
    while keep_pressing:
        win_tool.send_key_to_all_windows(window_name, key_code)
        time.sleep(interval)


def validate_float(value_if_allowed):
    if value_if_allowed == "":
        return True
    try:
        float(value_if_allowed)
        return True
    except ValueError:
        return False


def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# 打印选择的数组内容
def print_selected_value():
    selected_index = combobox.current()  # 获取选择框的当前下标
    log3.console(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]
    win_tool.activate_window(hwnd)


def hwnd_name_bind():
    global hwnd_array
    global hwnd_array_str

    s_inx = combobox.current()
    hwnd = hwnd_array[s_inx]

    hwnd_array = win_tool.get_all_window_handles_by_name(window_name)
    if None is hwnd_array or 0 == len(hwnd_array):
        hwnd_array = ["未找到刀剑2 窗口"]

    is_f = False
    for i in range(len(hwnd_array)):
        if hwnd == hwnd_array[i]:
            is_f = True
            break

    name = ""
    if is_f:
        name = dao2_common.get_hwnd_name_by_mounts(hwnd)
        print(name)
        dao2_common.set_hwnd_name(hwnd, name)

    # 搞一个新的窗口名称列表
    new_h_arr_s = []
    for i in range(len(hwnd_array)):
        if hwnd == hwnd_array[i]:
            new_h_arr_s.append(f"{hwnd}-{name}")
        else:
            na = ""
            for k in range(len(hwnd_array_str)):
                # 窗口句柄名称和
                h_a = f"{hwnd_array_str[k]}".split("-")
                if int(h_a[0]) == hwnd_array[i]:
                    if 2 == len(h_a):
                        na = h_a[1]
                    break
            if "" != na:
                new_h_arr_s.append(f"{hwnd_array[i]}-{na}")
            else:
                new_h_arr_s.append(f"{hwnd_array[i]}")
    hwnd_array_str = new_h_arr_s
    combobox['values'] = hwnd_array_str
    combobox.set(hwnd_array_str[s_inx])


def everyday_get_task(name):
    log3.console(name)
    with dao2_everyday.lock:
        if dao2_everyday.is_run:
            dao2_everyday.is_run = False
            return
        else:
            dao2_everyday.is_run = True

    if "九凤" == name:
        dao2_everyday.jiu_feng_task(hwnd_array)

    if "鸟山" == name:
        dao2_everyday.niao_shan_task(hwnd_array)


current_live_script_name = ""


def live_script(name):
    global current_live_script_name
    selected_index = combobox.current()  # 获取选择框的当前下标
    log3.console(f"选择的下标：{selected_index} - {name}")
    hwnd = hwnd_array[selected_index]

    current_live_script_name = name

    with dao2_wa_gancao.lock:
        if "挖大黄" == name:
            dao2_wa_dahuang.is_run = not dao2_wa_dahuang.is_run
            if dao2_wa_dahuang.is_run:
                dao2_wa_dahuang.wa_da_huang(hwnd)
                btn_wa_da_huang.config(bg="red")
            else:
                btn_wa_da_huang.config(bg="white")

        if "挖甘草" == name:
            dao2_wa_gancao.is_run = not dao2_wa_gancao.is_run
            if dao2_wa_gancao.is_run:
                btn_wa_gan_cao.config(bg="red")
                dao2_wa_gancao.gather(hwnd)
            else:
                btn_wa_gan_cao.config(bg="white")

        if "挖麻黄" == name:
            dao2_wa_ma_huang.is_run = not dao2_wa_ma_huang.is_run
            if dao2_wa_ma_huang.is_run:
                btn_wa_ma_huang.config(bg="red")
                dao2_wa_ma_huang.gather(hwnd)
            else:
                btn_wa_ma_huang.config(bg="white")

        if "挖白术" == name:
            dao2_wa_baishu.is_run = not dao2_wa_baishu.is_run
            if dao2_wa_baishu.is_run:
                btn_wa_bai_shu.config(bg="red")
                dao2_wa_baishu.gather(hwnd)
            else:
                btn_wa_bai_shu.config(bg="white")

        if "挖五味草" == name:
            dao2_wa_wuweicao.is_run = not dao2_wa_wuweicao.is_run
            if dao2_wa_wuweicao.is_run:
                btn_wa_wu_wei_cao.config(bg="red")
                dao2_wa_wuweicao.gather(hwnd)
            else:
                btn_wa_wu_wei_cao.config(bg="white")

        if "挖当归黄连" == name:
            dao2_wa_danghuang.is_run = not dao2_wa_danghuang.is_run
            if dao2_wa_danghuang.is_run:
                btn_wa_dang_huang.config(bg="red")
                dao2_wa_danghuang.gather(hwnd)
            else:
                btn_wa_dang_huang.config(bg="white")

        if "挖柴胡" == name:
            dao2_wa_chaihu.is_run = not dao2_wa_chaihu.is_run
            if dao2_wa_chaihu.is_run:
                btn_wa_chai_hu.config(bg="red")
                dao2_wa_chaihu.gather(hwnd)
            else:
                btn_wa_chai_hu.config(bg="white")

        if "挖川穹" == name:
            dao2_wa_chuanqiong.is_run = not dao2_wa_chuanqiong.is_run
            if dao2_wa_chuanqiong.is_run:
                btn_wa_chuan_qiong.config(bg="red")
                dao2_wa_chuanqiong.gather(hwnd)
            else:
                btn_wa_chuan_qiong.config(bg="white")

        if "挖金线莲" == name:
            dao2_wa_jinxianlian.is_run = not dao2_wa_jinxianlian.is_run
            if dao2_wa_jinxianlian.is_run:
                btn_wa_jin_xian_lian.config(bg="red")
                dao2_wa_jinxianlian.gather(hwnd)
            else:
                btn_wa_jin_xian_lian.config(bg="white")

        if "挖半夏" == name:
            dao2_wa_banxia.is_run = not dao2_wa_banxia.is_run
            if dao2_wa_banxia.is_run:
                btn_wa_ban_xia.config(bg="red")
                dao2_wa_banxia.gather(hwnd)
            else:
                btn_wa_ban_xia.config(bg="white")

        if "挖牛筋草" == name:
            dao2_wa_niu_jin_cao.is_run = not dao2_wa_niu_jin_cao.is_run
            if dao2_wa_niu_jin_cao.is_run:
                btn_wa_niu_jin_cao.config(bg="red")
                dao2_wa_niu_jin_cao.gather(hwnd)
            else:
                btn_wa_niu_jin_cao.config(bg="white")


current_kuang_shi_name = ""


def wa_kuang_shi(name):
    global current_kuang_shi_name
    hwnd = hwnd_array[combobox.current()]
    current_kuang_shi_name = name

    with dao2_wa_gancao.lock:
        if "挖栖魂矿石" == name:
            dao2_wa_xi_hun_kuangshi.is_run = not dao2_wa_xi_hun_kuangshi.is_run
            if dao2_wa_xi_hun_kuangshi.is_run:
                dao2_wa_xi_hun_kuangshi.gather(hwnd)
                btn_wa_xi_hun_kuang_shi.config(bg="red")
            else:
                btn_wa_xi_hun_kuang_shi.config(bg="white")


def gu_cheng_collect():
    selected_index = combobox.current()  # 获取选择框的当前下标
    print(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]

    with LOCK_GLOBAL_UI:
        dao2_gu_cheng.is_run = not dao2_gu_cheng.is_run
        if dao2_gu_cheng.is_run:
            btn_gu_cheng.config(bg="red")
            dao2_gu_cheng.gu_cheng_collect(hwnd)
        else:
            btn_gu_cheng.config(bg="white")


def gu_cheng_treasure():
    selected_index = combobox.current()  # 获取选择框的当前下标
    print(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]

    with LOCK_GLOBAL_UI:
        dao2_gu_cheng_treasure.is_run = not dao2_gu_cheng_treasure.is_run
        if dao2_gu_cheng_treasure.is_run:
            btn_gu_cheng_treasure.config(bg="red")
            dao2_gu_cheng_treasure.gu_cheng_treasure(hwnd)
        else:
            btn_gu_cheng_treasure.config(bg="white")


def da_qun_xia():
    selected_index = combobox.current()  # 获取选择框的当前下标
    print(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]

    with LOCK_GLOBAL_UI:
        # 窗口已经在打时才会关，不再打则开，支持多窗口同时打
        if hwnd in dao2_da_qunxia.run_hwnd:
            dao2_da_qunxia.is_run = not dao2_da_qunxia.is_run
        else:
            dao2_da_qunxia.is_run = True

        if dao2_da_qunxia.is_run:
            btn_xun_xia.config(bg="red")
            dao2_da_qunxia.start_da_qun_xia(hwnd)
        else:
            btn_xun_xia.config(bg="white")


def single_arena():
    selected_index = combobox.current()
    hwnd = hwnd_array[selected_index]

    with LOCK_GLOBAL_UI:
        dao2_arena.is_run = not dao2_arena.is_run
        if dao2_arena.is_run:
            btn_single_arena.config(bg="red")
            dao2_arena.start_arena([hwnd])
        else:
            btn_single_arena.config(bg="white")


def cao_yao_yan_mo():
    selected_index = combobox.current()  # 获取选择框的当前下标
    print(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]

    with LOCK_GLOBAL_UI:
        dao2_quick.is_run_cao_yao_yan_mo = not dao2_quick.is_run_cao_yao_yan_mo
        if dao2_quick.is_run_cao_yao_yan_mo:
            btn_yan_mo.config(bg="red")
            t = threading.Thread(target=dao2_quick.cao_yao_yan_mo, args=(hwnd,), daemon=True)
            t.start()
        else:
            btn_yan_mo.config(bg="white")


def arena():
    with LOCK_GLOBAL_UI:
        dao2_arena.is_run = not dao2_arena.is_run
        if dao2_arena.is_run:
            btn_arena.config(bg="red")
            dao2_arena.start_arena(hwnd_array)
        else:
            btn_arena.config(bg="white")


def huan_qian(name):
    selected_index = combobox.current()  # 获取选择框的当前下标
    hwnd = hwnd_array[selected_index]
    print(f"换钱 {selected_index} - {hwnd} - {name}")
    with LOCK_GLOBAL_UI:
        if "" == name:
            if dao2_quick.is_run_yi_jie_huan_qian:
                dao2_quick.is_run_yi_jie_huan_qian = not dao2_quick.is_run_yi_jie_huan_qian
                btn_yi_jie_wallet.config(bg="white")

            if dao2_quick.is_run_han_shui_huan_qian:
                dao2_quick.is_run_han_shui_huan_qian = not dao2_quick.is_run_han_shui_huan_qian
                btn_han_shui_wallet.config(bg="white")

            if dao2_quick.is_run_gu_cha_huan_qian:
                dao2_quick.is_run_gu_cha_huan_qian = not dao2_quick.is_run_gu_cha_huan_qian
                btn_gu_cha_wallet.config(bg="white")
            return

        if "异界" == name:
            dao2_quick.is_run_yi_jie_huan_qian = not dao2_quick.is_run_yi_jie_huan_qian
            if dao2_quick.is_run_yi_jie_huan_qian:
                btn_yi_jie_wallet.config(bg="red")
                t = threading.Thread(target=dao2_quick.yi_jie_huan_qian, args=(hwnd,), daemon=True)
                t.start()
            else:
                btn_yi_jie_wallet.config(bg="white")

        if "罕水" == name:
            dao2_quick.is_run_han_shui_huan_qian = not dao2_quick.is_run_han_shui_huan_qian
            if dao2_quick.is_run_han_shui_huan_qian:
                btn_han_shui_wallet.config(bg="red")
                t = threading.Thread(target=dao2_quick.han_shui_huan_qian, args=(hwnd,), daemon=True)
                t.start()
            else:
                btn_han_shui_wallet.config(bg="white")
        if "古刹" == name:
            dao2_quick.is_run_gu_cha_huan_qian = not dao2_quick.is_run_gu_cha_huan_qian
            if dao2_quick.is_run_gu_cha_huan_qian:
                btn_gu_cha_wallet.config(bg="red")
                t = threading.Thread(target=dao2_quick.gu_cha_huan_qian, args=(hwnd,), daemon=True)
                t.start()
            else:
                btn_gu_cha_wallet.config(bg="white")


def on_closing():
    log3.console("关闭所有线程，确保程序完全退出")
    global keep_pressing
    app.is_run_active_game_window = False
    app.is_run_release = False

    dao2_quick.runningCollect = False
    keep_pressing = False
    dao2_wa_dahuang.is_run = False
    dao2_wa_gancao.is_run = False
    dao2_wa_ma_huang.is_run = False
    dao2_wa_baishu.is_run = False
    dao2_wa_wuweicao.is_run = False
    dao2_wa_danghuang.is_run = False
    dao2_wa_chaihu.is_run = False
    dao2_wa_chuanqiong.is_run = False
    dao2_wa_jinxianlian.is_run = False
    dao2_wa_banxia.is_run = False
    dao2_wa_niu_jin_cao.is_run = False
    dao2_wa_xi_hun_kuangshi.is_run = False

    i_mouse.is_run_mouse_right_click = False
    i_mouse.is_run_mouse_left_click = False

    dao2_everyday.is_run = False
    dao2_gu_cheng.is_run = False
    dao2_gu_cheng_treasure.is_run = False

    dao2_quick.is_run_receive_notify = False
    dao2_quick.is_run_send_key_by_hwnd = False
    dao2_quick.is_run_cao_yao_yan_mo = False
    dao2_quick.is_auto_team = False

    dao2_quick.is_run_han_shui_huan_qian = False
    dao2_quick.is_run_gu_cha_huan_qian = False
    dao2_quick.is_run_yi_jie_huan_qian = False

    dao2_quick.is_run_auto_say = False

    dao2_arena.is_run = False
    dao2_da_qunxia.is_run = False

    dao2_muye_fuwuqi.is_run = False

    dao2_equipage.is_run_ren_zhu = False
    dao2_equipage.is_run_qiang_hua = False
    dao2_six_contest.is_run = False

    root.destroy()


# stop_all_script 停止所有脚本
def stop_all_script(event=None):
    global current_live_script_name
    log3.console("stop_all_script")

    global keep_pressing

    if i_mouse.is_run_mouse_right_click:
        mouse_right_click()

    if i_mouse.is_run_mouse_left_click:
        mouse_left_click()

    if dao2_quick.is_run_receive_notify:
        receive_notify()

    if dao2_quick.is_run_send_key_by_hwnd:
        send_key_by_hwnd()

    if dao2_quick.is_run_cao_yao_yan_mo:
        cao_yao_yan_mo()

    if dao2_quick.is_auto_team:
        auto_team()

    if dao2_quick.runningCollect:
        toggle_collect()

    if keep_pressing:
        keep_sending_key()

    if dao2_muye_fuwuqi.is_run:
        my_fuwuqi()

    if dao2_arena.is_run:
        arena()

    if dao2_gu_cheng.is_run:
        gu_cheng_collect()

    if dao2_gu_cheng_treasure.is_run:
        gu_cheng_treasure()

    if dao2_da_qunxia.is_run:
        da_qun_xia()

    if dao2_wa_dahuang.is_run:
        live_script(current_live_script_name)

    if dao2_wa_gancao.is_run:
        live_script(current_live_script_name)

    if dao2_wa_ma_huang.is_run:
        live_script(current_live_script_name)

    if dao2_wa_baishu.is_run:
        live_script(current_live_script_name)

    if dao2_wa_wuweicao.is_run:
        live_script(current_live_script_name)

    if dao2_wa_danghuang.is_run:
        live_script(current_live_script_name)

    if dao2_wa_chaihu.is_run:
        live_script(current_live_script_name)

    if dao2_wa_chuanqiong.is_run:
        live_script(current_live_script_name)

    if dao2_wa_jinxianlian.is_run:
        live_script(current_live_script_name)

    if dao2_wa_banxia.is_run:
        live_script(current_live_script_name)

    if dao2_wa_niu_jin_cao.is_run:
        live_script(current_live_script_name)

    if dao2_wa_xi_hun_kuangshi.is_run:
        wa_kuang_shi(current_kuang_shi_name)

    if dao2_quick.is_run_auto_say:
        saying()

    if dao2_equipage.is_run_ren_zhu:
        ren_zhu()

    if dao2_equipage.is_run_qiang_hua:
        qiang_hua()

    if dao2_six_contest.is_run:
        six_contest()

    # 所有换钱线程
    huan_qian("")

    # 不改UI 的按钮
    dao2_everyday.is_run = False

    messagebox.showwarning("提示", "所有脚本已停止")


if __name__ == "__main__":

    # 创建 Tkinter GUI
    root = tk.Tk()
    root.title(app_const.APP_NAME)
    root.geometry(app_const.WINDOW_GEOMETRY)  # 调整窗口大小

    root.attributes('-alpha', 0.96)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 创建一个画布和滚动条
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 布局滚动条和画布
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # 绑定鼠标滚轮事件
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # frame 第一排按钮
    label = tk.Label(scrollable_frame, text=f"严正声明：\n"
                                            "       1.警告：该软件仅可用于娱乐、技术交流，用于牟利后果自负。\n"
                                            "       2.谨防诈骗：任何因为此软件向您索取钱财转账的，都是诈骗。可进入新手村或向三位内测获取。\n"
                                            "       3.软件基于 Python 3.10、PaddleOCR 2、OpenCV，ChatGPT 4.o 在开发过程中提供了巨大帮助。\n"
                                            "       4.开发软件的目的，使用视觉和键鼠模拟手段，解决一些游戏中重复性的事务，提高娱乐性。免费软件，一万年不变。老狗是新手村的狗，一万年不变。\n"
                                            f"       5.感谢 林X灵、臭X丶、三月X开 三位大侠在测试期间提供的帮助，至此，{app_const.VERSION} 为稳定版本，短期不再开发新功能（随缘）。\n"
                                            "       最后，一段旅程结束：241022 用三周把10年前的遗憾弥补一二。我也该再次出发，告辞，各位侠客，不说再见，江湖再会。\n",
                     fg="red", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    frame = tk.Frame(scrollable_frame)
    frame.pack(pady=10, anchor='w', fill='x')

    btn_topmost = tk.Button(frame, text="窗口置顶", width=14, height=1, command=toggle_topmost)
    btn_topmost.pack(side=tk.LEFT, padx=10)

    btn_mount = tk.Button(frame, text="全体上马(F9)", width=14, height=1, command=mount_all)
    btn_mount.pack(side=tk.LEFT, padx=10)

    # 鼠标操作
    btn_mouse_left_click = tk.Button(frame, text="鼠标左键连击(F6)", width=15, height=1, command=mouse_left_click)
    btn_mouse_left_click.pack(side=tk.LEFT, padx=10)

    btn_mouse_right_click = tk.Button(frame, text="鼠标右键连击(F7)", width=15, height=1, command=mouse_right_click)
    btn_mouse_right_click.pack(side=tk.LEFT, padx=10)

    # 第二排
    frame_mouse = tk.Frame(scrollable_frame)
    frame_mouse.pack(pady=10, anchor='w', fill='x')

    btn_say_switch = tk.Button(frame_mouse, text="关闭发言", width=14, height=1, command=say_switch)
    btn_say_switch.pack(side=tk.LEFT, padx=10)

    btn_collect = tk.Button(frame_mouse, text="全体拾取(F10)", width=14, height=1, command=toggle_collect)
    btn_collect.pack(side=tk.LEFT, padx=10)

    btn_receive_notify = tk.Button(frame_mouse, text="全体接任务/副本/哨箭(F4)", width=20, height=1,
                                   command=receive_notify)
    btn_receive_notify.pack(side=tk.LEFT, padx=10)

    btn_auto_team = tk.Button(frame_mouse, text="自动组队", width=14, height=1, command=auto_team)
    btn_auto_team.pack(side=tk.LEFT, padx=10)

    # input_frame 输入框和一直按键
    input_frame = tk.Frame(scrollable_frame)
    input_frame.pack(pady=10, side=tk.TOP, fill="x", anchor="w")

    input_entry = tk.Entry(input_frame, width=10)
    input_entry.pack(side=tk.LEFT, padx=10)

    btn_send_key = tk.Button(input_frame, text="发送按键", width=15, height=1, command=send_input_key)
    btn_send_key.pack(side=tk.LEFT)

    vcmd = (root.register(validate_float), '%P')
    num_entry = tk.Entry(input_frame, width=5, validate="key", validatecommand=vcmd)
    num_entry.pack(side=tk.LEFT, padx=10)
    num_entry.insert(0, "0.02")

    btn_keep_pressing = tk.Button(input_frame, text="一直按键", width=15, height=1, command=keep_sending_key)
    btn_keep_pressing.pack(side=tk.LEFT)

    # everyday 日常
    frame_everyday = tk.Frame(scrollable_frame)
    frame_everyday.pack(pady=10, anchor='w', fill='x')

    btn_dance = tk.Button(frame_everyday, text="琼云跳舞", width=15, height=1,
                          command=lambda: dao2_everyday.start_qion_yun_dance(hwnd_array))
    btn_dance.pack(side=tk.LEFT, padx=10)

    btn_arena = tk.Button(frame_everyday, text="多开段位赛", width=15, height=1, command=arena)
    btn_arena.pack(side=tk.LEFT, padx=10)

    btn_jiufeng = tk.Button(frame_everyday, text="群接九凤", width=15, height=1,
                            command=lambda: everyday_get_task("九凤"))
    btn_jiufeng.pack(side=tk.LEFT, padx=10)

    btn_niaoshan = tk.Button(frame_everyday, text="群接鸟山", width=15, height=1,
                             command=lambda: everyday_get_task("鸟山"))
    btn_niaoshan.pack(side=tk.LEFT, padx=10)

    #  label 说明

    label_frame = tk.Frame(scrollable_frame)
    label_frame.pack(pady=10, side=tk.TOP, fill='x', anchor='w')

    label = tk.Label(label_frame,
                     text="使用说明：1.画面模式设置窗口最大。2.土遁放快捷栏不要被快捷键挡住。3.马放=快捷键位置。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame,
                     text="分辨率适配：游戏和屏幕要设置相同分辨率。1920*1080（1080P） 不缩放。2560*140（2k）放大125%。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="后台脚本：windows 本身键盘鼠标操作是流式的，即使脚本切换到后台也会一定程度上受前台键鼠操作的影响。"
                                       "\n    例如古城捡卷，开启后等脚本土遁操作进入进度条时就可以通过 alt+tab 切换到别的窗口去，游戏和脚本进入后台模式。"
                                       "\n    如果切换到后台后频繁按住键盘会发生意外情况：例如后台游戏脚本正好在输入坐标，那么这些按键就会错误的被发送到坐标输入框。"
                                       "\n    脚本和游戏在后台运行时，用电脑看电影、小说或者其它不频繁操作键鼠的动作，就不会有影响。"
                                       "\n    支持后台的脚本，也支持前台，前台会更稳定，但不能动键盘鼠标。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="停止脚本：快捷键 F12 停止所有脚本，请确保该快捷键未发生冲突。", fg="blue",
                     anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="全体上马：所有窗口后台发送 =，使用前需要把马放在 = 快捷键。（触发快捷键是 F9）。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame,
                     text="全体拾取：所有窗口后台发送 F8，使用前需要把拾取按键由默认的 Z 改为 F8。（开关快捷键是 F10）。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="全体接任务/副本/哨箭：主号分享任务/副本传送/放哨箭，其它号自动接受。后台运行。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="发送按键：所有窗口后台发送输入的按键（第一个输入框），不支持组合键。", fg="blue",
                     anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame,
                     text="一直按键：所有窗口后台发送输入的按键。一直按键根据间隔时间(秒)（第二个输入框）不断发送。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame,
                     text="鼠标左键连击：把鼠标移动到想要点击的目标上，按 F6 开始/停止 点击。理论每秒点击200次。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame,
                     text="鼠标右键连击：把鼠标移动到想要点击的目标上，按 F7 开始/停止 点击。理论每秒点击200次。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="多开段位赛：(会与单开段位赛冲突，同一时间只能使用一个)技能 123467890 ，怒气技能 5。纯后台模式。", fg="blue", anchor='w',
                     justify='left')
    label.pack(fill='x', pady=1)

    # 窗口句柄选择, 以及之后的单控选项
    # 添加下拉选择框和按钮
    selection_frame = tk.Frame(scrollable_frame)
    selection_frame.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    hwnd_array = win_tool.get_all_window_handles_by_name(window_name)
    if None is hwnd_array or 0 == len(hwnd_array):
        hwnd_array = ["未找到刀剑2 窗口"]
    hwnd_array_str = list(hwnd_array)

    # 创建下拉选择框
    combobox = ttk.Combobox(selection_frame, values=hwnd_array_str, width=20, state="readonly")
    combobox.current(0)  # 默认选择第一个元素
    combobox.pack(side=tk.LEFT, padx=10)

    btn_print_selection = tk.Button(selection_frame, text="激活窗口(后面的功能基于此窗口)", width=28, height=1,
                                    command=print_selected_value)
    btn_print_selection.pack(side=tk.LEFT, padx=10)

    btn_bind_role = tk.Button(selection_frame, text="刷新窗口", width=12, height=1, command=hwnd_name_bind)
    btn_bind_role.pack(side=tk.LEFT, padx=10)

    label = tk.Label(scrollable_frame,
                     text="单控说明：挖草药、古城捡卷等是单控，用前先选择一个窗口，脚本作用于此窗口（如不确定是哪个窗口，可以先激活确定）。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(scrollable_frame,
                     text="打群侠：打群侠会每秒使用 1234567890- 等技能，请确保这些快捷键放了合适的技能（）。", fg="blue",
                     anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(scrollable_frame, text="古城捡卷：到古城捡到一定数量会回瓦当存仓库，注意清理出仓库位置。（纯后台模式）",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(scrollable_frame,
                     text="古城挖宝：不要把凝神宝袋吃满，否则无法自动删除凝神宝袋。2级粽子放在无遮挡快捷栏（不足时自动吃）。到古城挖宝，V 挖藏宝图，R 技能打开宝箱，E 攻击哈桑。（纯后台模式）",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(scrollable_frame,
                     text="换钱袋子：找NPC打开商店，打开脚本，第一次检测鼠标位置后就会自动点击。可以同时不同窗口换不同商店的钱袋子，纯后台运行。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(scrollable_frame, text="挖草药：大黄、甘草，需要把神仙索定位在【607,830】(碎木)位置。神仙索要放在无快捷键遮挡的快捷栏。\n"
                                            "           麻黄、白术、五味草 直接土遁朝歌。\n"
                                            "           当归黄连、柴胡、川穹 需要神仙索记录在瓦洛古道【1300,1082】位置。\n"
                                            "           金线莲、半夏 需要神仙索记录在三春湖【422,1202】位置。\n"
                                            "           牛筋草 需要神仙索记录在三春湖【1778,259】位置，另放个技能在 1 快捷键位置，检测到敌人会自动攻击（远程攻击为上）。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    # 各种生活单控脚本
    live_frame = tk.Frame(scrollable_frame)
    live_frame.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    btn_wa_da_huang = tk.Button(live_frame, text="挖大黄", width=7, height=1, command=lambda: live_script("挖大黄"))
    btn_wa_da_huang.pack(side=tk.LEFT, padx=10)

    btn_wa_gan_cao = tk.Button(live_frame, text="挖甘草", width=7, height=1, command=lambda: live_script("挖甘草"))
    btn_wa_gan_cao.pack(side=tk.LEFT, padx=10)

    btn_wa_ma_huang = tk.Button(live_frame, text="挖麻黄", width=7, height=1, command=lambda: live_script("挖麻黄"))
    btn_wa_ma_huang.pack(side=tk.LEFT, padx=10)

    btn_wa_bai_shu = tk.Button(live_frame, text="挖白术", width=7, height=1, command=lambda: live_script("挖白术"))
    btn_wa_bai_shu.pack(side=tk.LEFT, padx=10)

    btn_wa_wu_wei_cao = tk.Button(live_frame, text="挖五味草", width=8, height=1,
                                  command=lambda: live_script("挖五味草"))
    btn_wa_wu_wei_cao.pack(side=tk.LEFT, padx=10)

    btn_wa_dang_huang = tk.Button(live_frame, text="挖当归黄连", width=9, height=1,
                                  command=lambda: live_script("挖当归黄连"))
    btn_wa_dang_huang.pack(side=tk.LEFT, padx=10)

    btn_wa_chai_hu = tk.Button(live_frame, text="挖柴胡", width=7, height=1, command=lambda: live_script("挖柴胡"))
    btn_wa_chai_hu.pack(side=tk.LEFT, padx=10)

    live_frame2 = tk.Frame(scrollable_frame)
    live_frame2.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    btn_wa_chuan_qiong = tk.Button(live_frame2, text="挖川穹", width=7, height=1, command=lambda: live_script("挖川穹"))
    btn_wa_chuan_qiong.pack(side=tk.LEFT, padx=7)

    btn_wa_jin_xian_lian = tk.Button(live_frame2, text="挖金线莲", width=8, height=1,
                                     command=lambda: live_script("挖金线莲"))
    btn_wa_jin_xian_lian.pack(side=tk.LEFT, padx=7)

    btn_wa_ban_xia = tk.Button(live_frame2, text="挖半夏", width=7, height=1, command=lambda: live_script("挖半夏"))
    btn_wa_ban_xia.pack(side=tk.LEFT, padx=7)

    btn_wa_niu_jin_cao = tk.Button(live_frame2, text="挖牛筋草", width=8, height=1,
                                   command=lambda: live_script("挖牛筋草"))
    btn_wa_niu_jin_cao.pack(side=tk.LEFT, padx=7)

    # 小功能
    fun_frame = tk.Frame(scrollable_frame)
    fun_frame.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    btn_wa_xi_hun_kuang_shi = tk.Button(fun_frame, text="挖栖魂矿石", width=9, height=1,
                                        command=lambda: wa_kuang_shi("挖栖魂矿石"))
    btn_wa_xi_hun_kuang_shi.pack(side=tk.LEFT, padx=10)

    btn_yan_mo = tk.Button(fun_frame, text="研磨草药", width=8, height=1, command=cao_yao_yan_mo)
    btn_yan_mo.pack(side=tk.LEFT, padx=10)

    btn_gu_cheng = tk.Button(fun_frame, text="古城捡卷", width=8, height=1, command=gu_cheng_collect)
    btn_gu_cheng.pack(side=tk.LEFT, padx=10)

    btn_gu_cheng_treasure = tk.Button(fun_frame, text="古城挖宝", width=8, height=1, command=gu_cheng_treasure)
    btn_gu_cheng_treasure.pack(side=tk.LEFT, padx=10)

    btn_xun_xia = tk.Button(fun_frame, text="打群侠", width=7, height=1, command=da_qun_xia)
    btn_xun_xia.pack(side=tk.LEFT, padx=10)

    btn_single_arena = tk.Button(fun_frame, text="单开段位赛", width=10, height=1, command=single_arena)
    btn_single_arena.pack(side=tk.LEFT, padx=10)

    # 自动换钱
    fun_frame2 = tk.Frame(scrollable_frame)
    fun_frame2.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    btn_yi_jie_wallet = tk.Button(fun_frame2, text="异界换钱袋子", width=15, height=1,
                                  command=lambda: huan_qian("异界"))
    btn_yi_jie_wallet.pack(side=tk.LEFT, padx=10)

    btn_han_shui_wallet = tk.Button(fun_frame2, text="罕水换钱袋子", width=15, height=1,
                                    command=lambda: huan_qian("罕水"))
    btn_han_shui_wallet.pack(side=tk.LEFT, padx=10)

    btn_gu_cha_wallet = tk.Button(fun_frame2, text="古刹换钱袋子", width=15, height=1,
                                  command=lambda: huan_qian("古刹"))
    btn_gu_cha_wallet.pack(side=tk.LEFT, padx=10)

    # 牧野练副武器
    mu_ye_frame = tk.Frame(scrollable_frame)
    mu_ye_frame.pack(pady=10, side=tk.TOP, fill="x", anchor="w")

    vcmd = (root.register(validate_float), '%P')
    mu_ye_entry = tk.Entry(mu_ye_frame, width=10, validate="key", validatecommand=vcmd)
    mu_ye_entry.pack(side=tk.LEFT, padx=10)
    mu_ye_entry.insert(0, "27.5")

    btn_mu_ye = tk.Button(mu_ye_frame, text="牧野练副武", width=15, height=1, command=my_fuwuqi)
    btn_mu_ye.pack(side=tk.LEFT)

    input_hwnd_send_key = tk.Entry(mu_ye_frame, width=10)
    input_hwnd_send_key.pack(side=tk.LEFT, padx=10)
    input_hwnd_send_key.insert(0, "1")

    btn_hwnd_send_key = tk.Button(mu_ye_frame, text="指定窗口后台一直按键", width=20, height=1,
                                  command=send_key_by_hwnd)
    btn_hwnd_send_key.pack(side=tk.LEFT)

    info_frame1 = tk.Frame(scrollable_frame)
    info_frame1.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    label = tk.Label(info_frame1,
                     text="研磨草药：把 研磨 技能放在 X 快捷键，把草药【大黄、甘草】放在默认背包，点击即可开始（纯后台模式）。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(info_frame1,
                     text="牧野练副武：编辑连招放在快捷键 1 位置，按钮左侧输入框输入每次技能用时，到牧野可以自动练副武器、炼魂。（后台模式，只有炼魂时会短暂激活窗口0.3s）",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(info_frame1,
                     text="指定窗口后台一直按键：牧野左侧是每次间隔秒，右侧输入按键，会给指定的窗口后台不断按键。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    # 自动强化
    fun_frame_q_h = tk.Frame(scrollable_frame)
    fun_frame_q_h.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    btn_qiang_hua = tk.Button(fun_frame_q_h, text="装备强化", width=15, height=1, command=qiang_hua)
    btn_qiang_hua.pack(side=tk.LEFT, padx=10)

    btn_ren_zhu = tk.Button(fun_frame_q_h, text="装备认主", width=15, height=1, command=ren_zhu)
    btn_ren_zhu.pack(side=tk.LEFT, padx=10)

    info_frame_equ = tk.Frame(scrollable_frame)
    info_frame_equ.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    label = tk.Label(info_frame_equ,
                     text="装备强化：打开强化界面，放进装备，选好强化槽位，不建议关闭装备框（因为这里用到 AI 识图，保存强化弹窗是半透明的，不利于识图的准确性）。保留更高强化，到 +17 或者 + 10 停止。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(info_frame_equ,
                     text="装备认主：装备放在背包第一格，1 快捷键放生生造化丹，2 快捷键放认主技能。自动认主保留 7333...。",
                     fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    # 后台发言
    say_frame = tk.Frame(scrollable_frame)
    say_frame.pack(pady=10, side=tk.TOP, fill="x", anchor="w")

    label = tk.Label(say_frame, text="每", fg="black", anchor='w', justify='left')
    label.pack(side=tk.LEFT, padx=10)

    input_say_time = tk.Entry(say_frame, width=5, validate="key", validatecommand=(root.register(validate_float), '%P'))
    input_say_time.pack(side=tk.LEFT, padx=10)
    input_say_time.insert(0, "90")

    label = tk.Label(say_frame, text="秒，发言内容：", fg="black", anchor='w', justify='left')
    label.pack(side=tk.LEFT, padx=10)

    input_say_content = tk.Entry(say_frame, width=25)
    input_say_content.pack(side=tk.LEFT, padx=10)
    input_say_content.insert(0, "99j 求购老狗一只。")

    btn_start_say = tk.Button(say_frame, text="开始发言", width=14, height=1, command=saying)
    btn_start_say.pack(side=tk.LEFT)

    # 特殊功能
    fun_frame_special = tk.Frame(scrollable_frame)
    fun_frame_special.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    btn_six_contest = tk.Button(fun_frame_special, text="擂台6次工具人(杨万里)", width=18, height=1, command=six_contest)
    btn_six_contest.pack(side=tk.LEFT, padx=10)

    # 说明
    explain_frame = tk.Frame(scrollable_frame)
    explain_frame.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    label = tk.Label(explain_frame, text="古城挖宝 快捷栏：", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    explain_image3 = Image.open(win_tool.resource_path("img/gucheng_kuaijielan.png"))  # 使用 PIL 加载图片
    explain_image3 = explain_image3.resize((341, 112), Image.LANCZOS)  # 调整图片大小为 300x200 像素
    explain_photo3 = ImageTk.PhotoImage(explain_image3)
    label3 = tk.Label(explain_frame, image=explain_photo3).pack(side=tk.LEFT, padx=10)

    label = tk.Label(explain_frame, text="认主 快捷栏：", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    explain_image4 = Image.open(win_tool.resource_path("img/renzhukuaijiejian.png"))
    explain_image4 = explain_image4.resize((341, 112), Image.LANCZOS)
    explain_photo4 = ImageTk.PhotoImage(explain_image4)
    label3 = tk.Label(explain_frame, image=explain_photo4).pack(side=tk.LEFT, padx=10)

    # 底部
    # bottom_frame = tk.Frame(scrollable_frame)
    # bottom_frame.pack(pady=20, side=tk.TOP, fill="x", anchor="w")
    #
    # # 底部一张图
    # image = Image.open(win_tool.resource_path("img/shibadafutou.png"))  # 使用 PIL 加载图片
    # image = image.resize((186, 334), Image.LANCZOS)
    # photo = ImageTk.PhotoImage(image)
    # img_label = tk.Label(bottom_frame, image=photo).pack(side=tk.LEFT, padx=10)
    #
    # image2 = Image.open(win_tool.resource_path("img/yangwanli.png"))
    # image2 = image2.resize((200, 334), Image.LANCZOS)
    # photo2 = ImageTk.PhotoImage(image2)
    # img_label2 = tk.Label(bottom_frame, image=photo2).pack(side=tk.LEFT, padx=10)
    #
    # image3 = Image.open(win_tool.resource_path("img/dashicunlaogou.png"))
    # image3 = image3.resize((186, 334), Image.LANCZOS)
    # photo3 = ImageTk.PhotoImage(image3)
    # img_label3 = tk.Label(bottom_frame, image=photo3).pack(side=tk.LEFT, padx=10)


    # 绑定快捷键
    # 使用 keyboard 绑定全局快捷键
    keyboard.add_hotkey('F12', stop_all_script)
    keyboard.add_hotkey('F10', toggle_collect)
    keyboard.add_hotkey('F9', mount_all)
    keyboard.add_hotkey('F7', mouse_right_click)
    keyboard.add_hotkey('F6', mouse_left_click)
    keyboard.add_hotkey('F4', receive_notify)

    # root.bind_all('<KeyPress-F12>', stop_all_script)
    # root.bind_all('<KeyPress-F10>', toggle_collect)
    # root.bind_all('<KeyPress-F9>', mount_all)

    # 启动激活窗口，子线程
    t = threading.Thread(target=app.active_game_window, args=(hwnd_array[0], ), daemon=True)
    t.start()

    root.bind("<Button-1>", root_click)
    app.start_release_job()
    root.mainloop()
