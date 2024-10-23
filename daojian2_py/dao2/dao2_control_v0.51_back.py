import threading
import time
import tkinter as tk
from tkinter import messagebox
import win32gui
import win32con
import win32api

#window_name = "夏禹剑 - 刀剑2"
window_name = "刀剑2"

# 自动拾取：控制线程是否继续执行
runningCollect = False
lockCollect = threading.Lock()

# 全局变量用于控制“一直按键”子线程
keep_pressing = False

# 窗口置顶
topmost = False

# 建立虚拟键码字典，键是按键字符，值是对应的虚拟键码（全部小写）
key_map = {
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45, 'f': 0x46, 'g': 0x47,
    'h': 0x48, 'i': 0x49, 'j': 0x4A, 'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E,
    'o': 0x4F, 'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54, 'u': 0x55,
    'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59, 'z': 0x5A,
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35, '6': 0x36,
    '7': 0x37, '8': 0x38, '9': 0x39,
    'f1': 0x70, 'f2': 0x71, 'f3': 0x72, 'f4': 0x73, 'f5': 0x74, 'f6': 0x75,
    'f7': 0x76, 'f8': 0x77, 'f9': 0x78, 'f10': 0x79, 'f11': 0x7A, 'f12': 0x7B,
    'space': 0x20, 'enter': 0x0D, 'tab': 0x09, 'esc': 0x1B, 'backspace': 0x08,
    '=': 0xBB, '-': 0xBD, '[': 0xDB, ']': 0xDD, ';': 0xBA, "'": 0xDE,
    ',': 0xBC, '.': 0xBE, '/': 0xBF, '\\': 0xDC
}

# 获取所有符合窗口名称的句柄
def get_all_window_handles_by_name(window_name):
    window_handles = []

    def enum_windows_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd) and window_name in win32gui.GetWindowText(hwnd):
            window_handles.append(hwnd)

    win32gui.EnumWindows(enum_windows_callback, None)
    return window_handles

# 发送按键消息
def send_key_to_window(hwnd, key):
    # WM_KEYDOWN 和 WM_KEYUP 分别表示按下和松开按键
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, key, 0)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, key, 0)

def send_key_to_all_windows(window_name, key_to_send):
    window_handles = get_all_window_handles_by_name(window_name)
    if window_handles:
        for hwnd in window_handles:
            print(f"发送按键 {key_to_send} 到窗口句柄: {hwnd}")
            send_key_to_window(hwnd, key_to_send)
    else:
        print(f"未找到窗口名称包含 '{window_name}' 的窗口")

# 拾取
def collect():
    key_to_send = 0x77  # 虚拟键码 'F8'
    global window_name
    while runningCollect:
        send_key_to_all_windows(window_name, key_to_send)
        time.sleep(1)

# 启动和停止 collect 函数的控制函数
def toggle_collect(event=None):
    print(f"触发 toggle_collect")
    if event is not None and event.type != '2':  # 2表示 KeyPress 事件
        return

    with lockCollect:
        global runningCollect
        if not runningCollect:
            runningCollect = True
            btn_collect.config(text="全体拾取（已开启）")
            # 启动子线程
            t = threading.Thread(target=collect)
            t.start()
        else:
            runningCollect = False
            btn_collect.config(text="全体拾取（未开启）")

# 全体上马功能
def mount_all(event=None):
    print("触发全体上马")
    global window_name
    send_key_to_all_windows(window_name, 0xBB)

# 窗口置顶功能
def toggle_topmost():
    global topmost
    topmost = not topmost  # 切换置顶状态
    if topmost:
        root.attributes('-topmost', True)
        btn_topmost.config(text="取消置顶")
        print("窗口已置顶")
    else:
        root.attributes('-topmost', False)
        btn_topmost.config(text="窗口置顶")
        print("取消窗口置顶")

# 发送按键的功能
def send_input_key():
    input_value = input_entry.get().strip().lower()  # 获取输入框内容并转为小写
    if not input_value:
        print("输入框为空")
        return

    # 从字典中获取按键码
    key_code = key_map.get(input_value)
    if key_code:
        print(f"输入的内容：{input_value}，对应的按键码：{key_code}")
        send_key_to_all_windows(window_name, key_code)
    else:
        print(f"未找到对应的按键码：{input_value}")

# 一直按键功能，获取输入框数字并发送按键
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

        key_code = key_map.get(key_to_send)
        interval = float(num_input)  # 转换为浮点数

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

# 子线程，不断发送按键
def send_key_continuously(key_code, interval):
    global keep_pressing
    while keep_pressing:
        send_key_to_all_windows(window_name, key_code)
        time.sleep(interval)

# 验证输入框是否为数字或浮点数
def validate_float(value_if_allowed):
    if value_if_allowed == "":
        return True
    try:
        float(value_if_allowed)  # 尝试将输入转换为浮点数
        return True
    except ValueError:
        return False

# 关闭应用程序时进行的清理工作
def on_closing():
    print("关闭所有线程，确保程序完全退出")
    global runningCollect, keep_pressing
    # 关闭所有线程，确保程序完全退出
    runningCollect = False
    keep_pressing = False
    root.destroy()  # 关闭 Tkinter 窗口

# 创建 Tkinter GUI
root = tk.Tk()
root.title("刀剑2 群控 （大石村老狗 v0.51）")
root.geometry("550x300")  # 调整窗口大小以适应新内容

# 设置窗口的透明度
root.attributes('-alpha', 0.9)

# 绑定关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)

# 创建按钮容器框架
frame = tk.Frame(root)
frame.pack(pady=20)

# 创建窗口置顶按钮
btn_topmost = tk.Button(frame, text="窗口置顶", width=15, height=2, command=toggle_topmost)
btn_topmost.pack(side=tk.LEFT, padx=10)

# 创建全体拾取按钮并绑定 toggle_collect 函数
btn_collect = tk.Button(frame, text="全体拾取（未开启）", width=15, height=2, command=toggle_collect)
btn_collect.pack(side=tk.LEFT, padx=10)

# 创建全体上马按钮并绑定 mount_all 函数
btn_mount = tk.Button(frame, text="全体上马", width=15, height=2, command=mount_all)
btn_mount.pack(side=tk.LEFT, padx=10)

# 创建输入框和发送按键按钮
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

# 输入框 (长度限制为 10)
input_entry = tk.Entry(input_frame, width=10)
input_entry.pack(side=tk.LEFT, padx=10)

# 发送按键按钮
btn_send_key = tk.Button(input_frame, text="发送按键", width=15, height=2, command=send_input_key)
btn_send_key.pack(side=tk.LEFT)

# 数字输入框 (宽度为 5，验证为浮点数)
vcmd = (root.register(validate_float), '%P')
num_entry = tk.Entry(input_frame, width=5, validate="key", validatecommand=vcmd)
num_entry.pack(side=tk.LEFT, padx=10)
num_entry.insert(0, "0.02")

# 一直按键按钮
btn_keep_pressing = tk.Button(input_frame, text="一直按键", width=15, height=2, command=keep_sending_key)
btn_keep_pressing.pack(side=tk.LEFT)

# 创建文本提示标签
label = tk.Label(root, text="全体拾取：所有窗口后台发送 F8，使用前需要把拾取按键由默认的 Z 改为 F8。（开关快捷键是 F10）。", fg="blue", anchor='w', justify='left')
label.pack(fill='x', pady=1)

label = tk.Label(root, text="全体上马：所有窗口后台发送 =，使用前需要把马放在 = 快捷键。（触发快捷键是 F9）。", fg="blue", anchor='w', justify='left')
label.pack(fill='x', pady=1)

label = tk.Label(root, text="发送按键：所有窗口后台发送输入的按键（第一个输入框），不支持组合键。", fg="blue", anchor='w', justify='left')
label.pack(fill='x', pady=1)

label = tk.Label(root, text="一直按键：所有窗口后台发送输入的按键。一直按键根据间隔时间(秒)（第二个输入框）不断发送。", fg="blue", anchor='w', justify='left')
label.pack(fill='x', pady=1)


# 绑定 F10 快捷键到 toggle_collect 函数，只在按下时触发
root.bind('<KeyPress-F10>', toggle_collect)

# F9 上马
root.bind('<KeyPress-F9>', mount_all)

# 运行 Tkinter 主事件循环
root.mainloop()
