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


#window_name = "夏禹剑 - 刀剑2"
window_name = "刀剑2"

# 自动拾取：控制线程是否继续执行
runningCollect = False
lockCollect = threading.Lock()

# 全局变量用于控制“一直按键”子线程
keep_pressing = False

# 窗口置顶
topmost = False

# 窗口句柄
hwnd_array = []

# 全局UI控制锁
LOCK_GLOBAL_UI = threading.Lock()


def collect():
    key_to_send = 0x77  # 虚拟键码 'F8'
    global window_name
    while runningCollect:
        win_tool.send_key_to_all_windows(window_name, key_to_send)
        time.sleep(1)


def toggle_collect(event=None):
    print(f"触发 toggle_collect")
    if event is not None and event.type != '2':  # 2表示 KeyPress 事件
        return

    with lockCollect:
        global runningCollect
        if not runningCollect:
            runningCollect = True
            btn_collect.config(bg="red")
            t = threading.Thread(target=collect, daemon=True)
            t.start()
        else:
            runningCollect = False
            btn_collect.config(bg="white")


def mount_all(event=None):
    print("触发全体上马")
    global window_name
    win_tool.send_key_to_all_windows(window_name, 0xBB)


def receive_notify(event=None):
    print("receive_notify 接通知")
    with LOCK_GLOBAL_UI:
        dao2_quick.is_run_receive_notify = not dao2_quick.is_run_receive_notify
        print(f"receive_notify {dao2_quick.is_run_receive_notify}")

    with dao2_quick.lock:
        if dao2_quick.is_run_receive_notify:
            btn_receive_notify.config(bg="red")
            t = threading.Thread(target=dao2_quick.receive_notify(hwnd_array), args=(hwnd_array,), daemon=True)
            t.start()
        else:
            btn_receive_notify.config(bg="white")


def mouse_right_click(event=None):
    with LOCK_GLOBAL_UI:
        i_mouse.is_run_mouse_right_click = not i_mouse.is_run_mouse_right_click
        print(f"鼠标右键点击{i_mouse.is_run_mouse_right_click}")

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
        print(f"鼠标左键点击{i_mouse.is_run_mouse_left_click}")
    interval = 0.05
    with i_mouse.lock_run_mouse_left_click:
        if i_mouse.is_run_mouse_left_click:
            btn_mouse_left_click.config(bg="red")
            t = threading.Thread(target=i_mouse.while_mouse_left_click, args=(interval,), daemon=True)
            t.start()
        else:
            btn_mouse_left_click.config(bg="white")


def toggle_topmost():
    global topmost
    topmost = not topmost
    if topmost:
        root.attributes('-topmost', True)
        btn_topmost.config(text="取消置顶")
        print("窗口已置顶")
    else:
        root.attributes('-topmost', False)
        btn_topmost.config(text="窗口置顶")
        print("取消窗口置顶")


def send_input_key():
    input_value = input_entry.get().strip().lower()
    if not input_value:
        print("输入框为空")
        return

    key_code = win_tool.key_map.get(input_value)
    if key_code:
        print(f"输入的内容：{input_value}，对应的按键码：{key_code}")
        win_tool.send_key_to_all_windows(window_name, key_code)
    else:
        print(f"未找到对应的按键码：{input_value}")

def keep_sending_key():
    global keep_pressing
    keep_pressing = not keep_pressing

    if keep_pressing:
        btn_keep_pressing.config(text="停止按键")
        key_to_send = input_entry.get().strip().lower()
        num_input = num_entry.get().strip()

        if not key_to_send or not num_input:
            print("按键或时间间隔输入无效")
            keep_pressing = False
            btn_keep_pressing.config(text="一直按键")
            return

        key_code = win_tool.key_map.get(key_to_send)
        interval = float(num_input)

        if key_code:
            print(f"开始不断发送按键：{key_code}，间隔：{interval} 秒")
            t = threading.Thread(target=send_key_continuously, args=(key_code, interval), daemon=True)
            t.start()
        else:
            print(f"未找到按键码：{key_to_send}")
            keep_pressing = False
            btn_keep_pressing.config(text="一直按键")
    else:
        btn_keep_pressing.config(text="一直按键")
        print("停止发送按键")


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
    print(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]
    win_tool.activate_window(hwnd)


def everyday_get_task(name):
    print(name)
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



def live_script(name):
    print(name)
    selected_index = combobox.current()  # 获取选择框的当前下标
    print(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]

    with dao2_wa_gancao.lock:
        if "挖大黄" == name:
            if dao2_wa_dahuang.is_run:
                dao2_wa_dahuang.is_run = False
            else:
                dao2_wa_dahuang.is_run = True
                dao2_wa_dahuang.wa_da_huang(hwnd)

        if "挖甘草" == name:
            if dao2_wa_gancao.is_run:
                dao2_wa_gancao.is_run = False
            else:
                dao2_wa_gancao.is_run = True
                dao2_wa_gancao.gather(hwnd)


def gu_cheng_collect():
    selected_index = combobox.current()  # 获取选择框的当前下标
    print(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]
    dao2_gu_cheng.gu_cheng_collect(hwnd)


def on_closing():
    print("关闭所有线程，确保程序完全退出")
    global runningCollect, keep_pressing
    runningCollect = False
    keep_pressing = False
    dao2_wa_dahuang.is_run = False
    dao2_wa_gancao.is_run = False

    i_mouse.is_run_mouse_right_click = False
    i_mouse.is_run_mouse_left_click = False

    dao2_everyday.is_run = False
    dao2_gu_cheng.is_run = False

    dao2_quick.is_run_receive_notify = False

    root.destroy()


# stop_all_script 停止所有脚本
def stop_all_script(event=None):
    print("stop_all_script")

    global runningCollect, keep_pressing

    if i_mouse.is_run_mouse_right_click:
        mouse_right_click()

    if i_mouse.is_run_mouse_left_click:
        mouse_left_click()

    if dao2_quick.is_run_receive_notify:
        receive_notify()

    if runningCollect:
        toggle_collect()

    if keep_pressing:
        keep_sending_key()

    # 不改UI 的按钮
    dao2_everyday.is_run = False
    dao2_gu_cheng.is_run = False
    dao2_wa_dahuang.is_run = False
    dao2_wa_gancao.is_run = False

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
    frame = tk.Frame(scrollable_frame)
    frame.pack(pady=10, anchor='w', fill='x')

    btn_topmost = tk.Button(frame, text="窗口置顶", width=15, height=1, command=toggle_topmost)
    btn_topmost.pack(side=tk.LEFT, padx=10)

    btn_mount = tk.Button(frame, text="全体上马(F9)", width=15, height=1, command=mount_all)
    btn_mount.pack(side=tk.LEFT, padx=10)

    # 鼠标操作
    btn_mouse_left_click = tk.Button(frame, text="鼠标左键连击(F6)", width=15, height=1, command=mouse_left_click)
    btn_mouse_left_click.pack(side=tk.LEFT, padx=10)

    btn_mouse_right_click = tk.Button(frame, text="鼠标右键连击(F7)", width=15, height=1, command=mouse_right_click)
    btn_mouse_right_click.pack(side=tk.LEFT, padx=10)

    # 第二排
    frame_mouse = tk.Frame(scrollable_frame)
    frame_mouse.pack(pady=10, anchor='w', fill='x')

    btn_collect = tk.Button(frame_mouse, text="全体拾取(F10)", width=15, height=1, command=toggle_collect)
    btn_collect.pack(side=tk.LEFT, padx=10)

    btn_receive_notify = tk.Button(frame_mouse, text="全体接任务/副本/哨箭(F4)", width=20, height=1, command=receive_notify)
    btn_receive_notify.pack(side=tk.LEFT, padx=10)

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

    btn_jiufeng = tk.Button(frame_everyday, text="群接九凤", width=15, height=1, command=lambda: everyday_get_task("九凤"))
    btn_jiufeng.pack(side=tk.LEFT, padx=10)

    btn_niaoshan = tk.Button(frame_everyday, text="群接鸟山", width=15, height=1, command=lambda: everyday_get_task("鸟山"))
    btn_niaoshan.pack(side=tk.LEFT, padx=10)

    #  label 说明

    label_frame = tk.Frame(scrollable_frame)
    label_frame.pack(pady=10, side=tk.TOP, fill='x', anchor='w')

    label = tk.Label(label_frame, text="使用说明：1.画面模式设置窗口最大。2.土遁放快捷栏不要被快捷键挡住。3.马放=快捷键位置。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="停止脚本：快捷键 F12 停止所有脚本，请确保该快捷键未发生冲突。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="全体上马：所有窗口后台发送 =，使用前需要把马放在 = 快捷键。（触发快捷键是 F9）。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="全体拾取：所有窗口后台发送 F8，使用前需要把拾取按键由默认的 Z 改为 F8。（开关快捷键是 F10）。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="全体接任务/副本/哨箭：主号分享任务/副本传送/放哨箭，其它号自动接受。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="发送按键：所有窗口后台发送输入的按键（第一个输入框），不支持组合键。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="一直按键：所有窗口后台发送输入的按键。一直按键根据间隔时间(秒)（第二个输入框）不断发送。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(label_frame, text="鼠标左键连击：把鼠标移动到想要点击的目标上，按 F6 开始/停止 点击。理论每秒点击200次。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)
    label = tk.Label(label_frame, text="鼠标右键连击：把鼠标移动到想要点击的目标上，按 F7 开始/停止 点击。理论每秒点击200次。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    # 窗口句柄选择, 以及之后的单控选项
    # 添加下拉选择框和按钮
    selection_frame = tk.Frame(scrollable_frame)
    selection_frame.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    hwnd_array = win_tool.get_all_window_handles_by_name(window_name)
    if None is hwnd_array:
        hwnd_array = ["未找到刀剑2 窗口"]

    # 创建下拉选择框
    combobox = ttk.Combobox(selection_frame, values=hwnd_array, width=15, state="readonly")
    combobox.current(0)  # 默认选择第一个元素
    combobox.pack(side=tk.LEFT, padx=10)

    btn_print_selection = tk.Button(selection_frame, text="激活窗口", width=15, height=1, command=print_selected_value)
    btn_print_selection.pack(side=tk.LEFT, padx=10)

    label = tk.Label(scrollable_frame, text="单控说明：挖草药、古城捡卷等是前台单控，用前先选择一个窗口，脚本作用于此窗口（如不确定是哪个窗口，可以先激活确定）。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    # 各种生活单控脚本
    live_frame = tk.Frame(scrollable_frame)
    live_frame.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    btn_wa_da_huang = tk.Button(live_frame, text="挖大黄", width=15, height=1, command=lambda: live_script("挖大黄"))
    btn_wa_da_huang.pack(side=tk.LEFT, padx=10)

    btn_wa_gan_cao = tk.Button(live_frame, text="挖甘草", width=15, height=1, command=lambda: live_script("挖甘草"))
    btn_wa_gan_cao.pack(side=tk.LEFT, padx=10)

    btn_gu_cheng = tk.Button(live_frame, text="古城捡卷", width=15, height=1, command=gu_cheng_collect)
    btn_gu_cheng.pack(side=tk.LEFT, padx=10)

    # 底部
    bottom_frame = tk.Frame(scrollable_frame)
    bottom_frame.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    # 底部一张图
    image = Image.open(win_tool.resource_path("img/shibadafutou.png"))  # 使用 PIL 加载图片
    image = image.resize((186, 334), Image.LANCZOS)  # 调整图片大小为 300x200 像素
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(bottom_frame, image=photo)
    label.pack(side=tk.LEFT, padx=10)  # 将 Label 添加到窗口并设置间距

    image2 = Image.open(win_tool.resource_path("img/dashicunlaogou.png"))  # 使用 PIL 加载图片
    image2 = image2.resize((186, 334), Image.LANCZOS)  # 调整图片大小为 300x200 像素
    photo2 = ImageTk.PhotoImage(image2)
    label2 = tk.Label(bottom_frame, image=photo2)
    label2.pack(side=tk.LEFT, padx=10)


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

    root.mainloop()
