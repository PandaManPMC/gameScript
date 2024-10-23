import threading
import time
import tkinter as tk
from tkinter import ttk  # 用于引入 Combobox
import win32gui
import keyboard
from tkinter import messagebox

import win_tool
import dao2_wa_dahuang


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

# 获取所有符合窗口名称的句柄
def get_all_window_handles_by_name(window_name):
    window_handles = []

    def enum_windows_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd) and window_name in win32gui.GetWindowText(hwnd):
            window_handles.append(hwnd)

    win32gui.EnumWindows(enum_windows_callback, None)
    return window_handles


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
            btn_collect.config(text="全体拾取（已开启）")
            t = threading.Thread(target=collect)
            t.start()
        else:
            runningCollect = False
            btn_collect.config(text="全体拾取（未开启）")


def mount_all(event=None):
    print("触发全体上马")
    global window_name
    win_tool.send_key_to_all_windows(window_name, 0xBB)


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
            t = threading.Thread(target=send_key_continuously, args=(key_code, interval))
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


def on_closing():
    print("关闭所有线程，确保程序完全退出")
    global runningCollect, keep_pressing
    runningCollect = False
    keep_pressing = False
    dao2_wa_dahuang.is_run_wa_da_huang = False
    root.destroy()


def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# 打印选择的数组内容
def print_selected_value():
    selected_index = combobox.current()  # 获取选择框的当前下标
    print(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]
    win_tool.activate_window(hwnd)


def live_script(name):
    print(name)
    selected_index = combobox.current()  # 获取选择框的当前下标
    print(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]

    if "挖大黄" == name:
        if dao2_wa_dahuang.is_run_wa_da_huang:
            dao2_wa_dahuang.is_run_wa_da_huang = False
        else:
            dao2_wa_dahuang.is_run_wa_da_huang = True
            dao2_wa_dahuang.wa_da_huang(hwnd)


# stop_all_script 停止所有脚本
def stop_all_script(event=None):
    print("stop_all_script")

    global runningCollect
    global keep_pressing
    dao2_wa_dahuang.is_run_wa_da_huang = False

    if runningCollect:
        toggle_collect()

    if keep_pressing:
        keep_sending_key()

    messagebox.showwarning("提示", "所有脚本已停止")


if __name__ == "__main__":

    # 创建 Tkinter GUI
    root = tk.Tk()
    root.title("刀剑2 群控 （大石村老狗 v0.51）")
    root.geometry("700x400")  # 调整窗口大小

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

    # 创建滚动内容框架中的元素
    frame = tk.Frame(scrollable_frame)
    frame.pack(pady=10)

    btn_topmost = tk.Button(frame, text="窗口置顶", width=15, height=1, command=toggle_topmost)
    btn_topmost.pack(side=tk.LEFT, padx=10)

    btn_collect = tk.Button(frame, text="全体拾取（未开启）", width=15, height=1, command=toggle_collect)
    btn_collect.pack(side=tk.LEFT, padx=10)

    btn_mount = tk.Button(frame, text="全体上马", width=15, height=1, command=mount_all)
    btn_mount.pack(side=tk.LEFT, padx=10)

    input_frame = tk.Frame(scrollable_frame)
    input_frame.pack(pady=10)

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

    label = tk.Label(scrollable_frame, text="全体拾取：所有窗口后台发送 F8，使用前需要把拾取按键由默认的 Z 改为 F8。（开关快捷键是 F10）。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(scrollable_frame, text="全体上马：所有窗口后台发送 =，使用前需要把马放在 = 快捷键。（触发快捷键是 F9）。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(scrollable_frame, text="发送按键：所有窗口后台发送输入的按键（第一个输入框），不支持组合键。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    label = tk.Label(scrollable_frame, text="一直按键：所有窗口后台发送输入的按键。一直按键根据间隔时间(秒)（第二个输入框）不断发送。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    # 添加下拉选择框和按钮
    selection_frame = tk.Frame(scrollable_frame)
    selection_frame.pack(pady=20)

    hwnd_array = win_tool.get_all_window_handles_by_name(window_name)
    if None is hwnd_array:
        hwnd_array = ["未找到刀剑2 窗口"]

    # 创建下拉选择框
    combobox = ttk.Combobox(selection_frame, values=hwnd_array, width=15, state="readonly")
    combobox.current(0)  # 默认选择第一个元素
    combobox.pack(side=tk.LEFT, padx=10)

    # 创建打印选择内容的按钮
    btn_print_selection = tk.Button(selection_frame, text="激活窗口", width=15, height=1, command=print_selected_value)
    btn_print_selection.pack(side=tk.LEFT, padx=10)

    label = tk.Label(scrollable_frame, text="停止脚本：快捷键 F12 理论上停止所有脚本，请确保该快捷键未发生冲突。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)
    label = tk.Label(scrollable_frame, text="单控说明：挖草药、古城捡卷等是前台单控，用前先选择一个窗口，脚本作用于此窗口（如不确定是哪个窗口，可以先激活确定）。", fg="blue", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    # 各种生活单控脚本
    live_frame = tk.Frame(scrollable_frame)
    live_frame.pack(pady=20)

    btn_wa_da_huang = tk.Button(live_frame, text="挖大黄", width=15, height=1, command=lambda: live_script("挖大黄"))
    btn_wa_da_huang.pack(side=tk.LEFT, padx=10)

    # 绑定快捷键
    # 使用 keyboard 绑定全局快捷键
    keyboard.add_hotkey('F12', stop_all_script)
    keyboard.add_hotkey('F10', toggle_collect)
    keyboard.add_hotkey('F9', mount_all)

    # root.bind_all('<KeyPress-F12>', stop_all_script)
    # root.bind_all('<KeyPress-F10>', toggle_collect)
    # root.bind_all('<KeyPress-F9>', mount_all)

    root.mainloop()
