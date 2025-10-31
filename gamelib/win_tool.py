import time

import win32gui
import win32con
import win32api
import ctypes
import pyautogui
import pyperclip
import os
import sys
from ctypes import windll, wintypes
import ctypes
import threading


lock = threading.RLock()


# 获取打包后资源的路径
def resource_path(relative_path):
    """获取资源文件的绝对路径，打包后也能正确访问"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后存放临时文件的路径
        base_path = sys._MEIPASS
    else:
        # 开发环境中的路径
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



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
    ',': 0xBC, '.': 0xBE, '/': 0xBF, '\\': 0xDC, "ctrl": 0xA2, "~": 0xC0, "`": 0xC0
}

# 启用 DPI 感知
ctypes.windll.shcore.SetProcessDpiAwareness(2)


# 获取屏幕缩放比例（基于主窗口）
def get_screen_scale(hwnd=None):
    if ctypes.windll.shcore is not None:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # 设置为每个监视器的 DPI 感知
    else:
        ctypes.windll.user32.SetProcessDPIAware()  # 设置为系统 DPI 感知
    # 如果传递了 hwnd，获取该窗口的 DPI，否则获取主显示器 DPI
    # hdc = None
    # if None is hwnd:
    #     hdc = ctypes.windll.user32.GetDC(0)
    # else:
    #     hdc = ctypes.windll.user32.GetDC(hwnd)
    # dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX, 88是水平DPI
    # if hwnd:
    #     ctypes.windll.user32.ReleaseDC(hwnd, hdc)
    # else:
    #     ctypes.windll.user32.ReleaseDC(0, hdc)

    if None is hwnd:
        hdc = ctypes.windll.user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
    else:
        dpi = ctypes.windll.user32.GetDpiForWindow(hwnd)

    # 计算缩放比例
    scale_factor = dpi / 96  # 96 DPI 是标准缩放（100%）
    print(scale_factor)
    return scale_factor


def get_screen_scale_by_desktop():
    if ctypes.windll.shcore is not None:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # 设置为每个监视器的 DPI 感知
    else:
        ctypes.windll.user32.SetProcessDPIAware()  # 设置为系统 DPI 感知
    hdc = ctypes.windll.user32.GetDC(0)
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
    scale_factor = dpi / 96
    print(scale_factor)
    return scale_factor


def calculate_physical_pixels(logical_pixels, scale_percentage):
    scale_factor = scale_percentage
    return int(logical_pixels / scale_factor)


def auto_pixels(x, hwnd=None):
    scale = get_screen_scale(hwnd)
    scale_desktop = get_screen_scale_by_desktop()
    if scale == scale_desktop:
        return x
    return int(x / scale_desktop)


# 物理分辨率偏移 （例如已经放大 125% 的坐标，返回真实的）
def calculate_physical_px(logical_pixels, hwnd=None):
    scale_percentage = get_screen_scale(hwnd)
    if 1 == scale_percentage:
        return logical_pixels
    scale_factor = scale_percentage
    return int(logical_pixels / scale_factor)


# 计算分辨率下的真实偏移(例如，125%放大，position 就会 * 125%)
def calculate_offset(position, hwnd=None):
    s = get_screen_scale(hwnd)
    if 1 == s:
        return position
    return int(position * s)


# 获取屏幕宽度和高度
def get_win_w_h():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)  # 参数 0 表示屏幕宽度
    screen_height = user32.GetSystemMetrics(1)  # 参数 1 表示屏幕高度
    return screen_width, screen_height


# 定义鼠标事件的常量
MOUSEEVENTF_MOVE = 0x0001  # 鼠标移动
MOUSEEVENTF_LEFTDOWN = 0x0002  # 鼠标左键按下
MOUSEEVENTF_LEFTUP = 0x0004  # 鼠标左键抬起
MOUSEEVENTF_ABSOLUTE = 0x8000  # 绝对坐标
MOUSEEVENTF_RIGHTDOWN = 0x0008  # 右键按下
MOUSEEVENTF_RIGHTUP = 0x0010    # 右键抬起
MOUSEEVENTF_MIDDLEDOWN = 0x0020     # 鼠标中键按下
MOUSEEVENTF_MIDDLEUP = 0x0040       # 鼠标中键抬起
MOUSEEVENTF_ABSOLUTE = 0x8000       # 绝对坐标模式
MOUSEEVENTF_WHEEL = 0x0800          # 鼠标滚轮
MOUSEEVENTF_HWHEEL = 0x01000        # 鼠标水平滚轮


# 定义 INPUT 和 MOUSEINPUT 结构体
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("mi", MOUSEINPUT)]

# 将坐标转换为绝对坐标
def absolute_coords(x, y):
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    abs_x = int(x * 65535 / screen_width)
    abs_y = int(y * 65535 / screen_height)
    return abs_x, abs_y


# 鼠标移动
def move_mouse(x, y):
    abs_x, abs_y = absolute_coords(x, y)
    # 模拟鼠标移动到指定位置
    mi_move = MOUSEINPUT(dx=abs_x, dy=abs_y, mouseData=0, dwFlags=MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, time=0,
                         dwExtraInfo=None)
    input_move = INPUT(type=0, mi=mi_move)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_move), ctypes.sizeof(input_move))


def mouse_left_click():
    # 模拟鼠标左键按下
    mi_down = MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_LEFTDOWN, time=0, dwExtraInfo=None)
    input_down = INPUT(type=0, mi=mi_down)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_down), ctypes.sizeof(input_down))

    # 模拟鼠标左键抬起
    mi_up = MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_LEFTUP, time=0, dwExtraInfo=None)
    input_up = INPUT(type=0, mi=mi_up)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_up), ctypes.sizeof(input_up))


# 模拟鼠标左键点击
def send_input_mouse_left_click(x, y):
    move_mouse(x, y)
    time.sleep(0.01)
    mouse_left_click()


def send_input_mouse_right_click(x, y):
    move_mouse(x, y)
    time.sleep(0.01)
    mouse_right_click()


def send_input_mouse_middle_click(x, y):
    move_mouse(x, y)
    time.sleep(0.01)
    mouse_middle_click()


def mouse_right_click():
    mi_down = MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_RIGHTDOWN, time=0, dwExtraInfo=None)
    input_down = INPUT(type=0, mi=mi_down)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_down), ctypes.sizeof(input_down))

    mi_up = MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_RIGHTUP, time=0, dwExtraInfo=None)
    input_up = INPUT(type=0, mi=mi_up)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_up), ctypes.sizeof(input_up))


def mouse_middle_click():
    mi_down = MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_MIDDLEDOWN, time=0, dwExtraInfo=None)
    input_down = INPUT(type=0, mi=mi_down)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_down), ctypes.sizeof(input_down))

    mi_up = MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_MIDDLEUP, time=0, dwExtraInfo=None)
    input_up = INPUT(type=0, mi=mi_up)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_up), ctypes.sizeof(input_up))


def click_right_current_position():
    x, y = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def click_left_current_position():
    x, y = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)



# 向上滚动鼠标滚轮
def scroll_mouse_up(amount):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, amount, 0)


# 向下滚动鼠标滚轮
def scroll_mouse_down(amount):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -amount, 0)


# 鼠标左键
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202


def send_mouse_left_click(hwnd, x, y):
    with lock:
        x = int(x)
        y = int(y)
        if is_window_foreground(hwnd):
            send_input_mouse_left_click(x, y)
        else:
            # print(f"x={x}, y={y} = {(y << 16) | x}")
            win32api.SendMessage(hwnd, WM_LBUTTONDOWN, 1, (y << 16) | x)
            time.sleep(0.02)
            win32api.SendMessage(hwnd, WM_LBUTTONUP, 0, (y << 16) | x)
        # l_param = (y << 16) | x
        # move_mouse_to(hwnd, x, y)
        # time.sleep(0.1)
        # ctypes.windll.user32.PostMessageW(hwnd, WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
        # ctypes.windll.user32.PostMessageW(hwnd, WM_LBUTTONUP, 0, l_param)
        '''
            SendMessage：发生鼠标事件，游戏窗口在前台时会发送失败，在后台就一定会发送成功。
            PostMessage：发生鼠标事件，可能丢失，因为是异步的。
        '''
        # win32api.SendMessage(hwnd, WM_LBUTTONDOWN, 1, (y << 16) | x)
        # win32api.SendMessage(hwnd, WM_LBUTTONUP, 0, (y << 16) | x)
        # ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
        # ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONUP, 0, l_param)


# 鼠标右键
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205


def send_mouse_right_click(hwnd, x, y):
    with lock:
        x = int(x)
        y = int(y)
        if is_window_foreground(hwnd):
            send_input_mouse_right_click(x, y)
        else:
            win32api.SendMessage(hwnd, WM_RBUTTONDOWN, 1, (y << 16) | x)
            win32api.SendMessage(hwnd, WM_RBUTTONUP, 0, (y << 16) | x)
    # with lock:
    #     x = int(x)
    #     y = int(y)
    #     l_param = (y << 16) | x
    #     ctypes.windll.user32.PostMessageW(hwnd, WM_RBUTTONDOWN, win32con.MK_RBUTTON, l_param)
    #     ctypes.windll.user32.PostMessageW(hwnd, WM_RBUTTONUP, 0, l_param)
    #     print(f"已向句柄 {hwnd} 发送右键点击事件")


# 鼠标中键
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208


def send_mouse_middle_click(hwnd, x, y):
    with lock:
        x = int(x)
        y = int(y)
        if is_window_foreground(hwnd):
            send_input_mouse_middle_click(x, y)
        else:
            l_param = (y << 16) | x
            ctypes.windll.user32.PostMessageW(hwnd, WM_MBUTTONDOWN, win32con.MK_MBUTTON, l_param)
            ctypes.windll.user32.PostMessageW(hwnd, WM_MBUTTONUP, 0, l_param)

# 定义鼠标移动消息
WM_MOUSEMOVE = 0x0200


def move_mouse_to(hwnd, x, y):
    with lock:
        x = int(x)
        y = int(y)
        l_param = (y << 16) | x
        # ctypes.windll.user32.SetWindowLongW(hwnd, win32con.GWL_EXSTYLE,
        #                                      ctypes.windll.user32.GetWindowLongW(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_NOACTIVATE)
        ctypes.windll.user32.PostMessageW(hwnd, WM_MOUSEMOVE, 0, l_param)


# 定义鼠标滚轮消息
WM_MOUSEWHEEL = 0x020A

def scroll_mouse_wheel_at(hwnd, x, y, scroll_amount=120):
    with lock:
        x = int(x)
        y = int(y)
        """
        在指定窗口和位置发送鼠标滚轮滚动事件
        :param hwnd: 目标窗口的句柄
        :param x: 滚轮滚动的位置的 x 坐标（相对于窗口）
        :param y: 滚轮滚动的位置的 y 坐标（相对于窗口）
        :param scroll_amount: 滚动的幅度，默认为 120（一个单位滚动）
        """
        w_param = (scroll_amount << 16)  # 向上滚动为正值，向下滚动为负值
        l_param = (y << 16) | x
        ctypes.windll.user32.PostMessageW(hwnd, WM_MOUSEWHEEL, w_param, l_param)


def send_mouse_wheel_at_sm(hwnd, x, y, scroll_amount=120):
    """
    在指定窗口和位置发送鼠标滚轮滚动事件（使用 win32api.SendMessage，同步发送）
    :param hwnd: 目标窗口句柄
    :param x: 滚轮滚动位置的 x 坐标（相对于窗口）
    :param y: 滚轮滚动位置的 y 坐标（相对于窗口）
    :param scroll_amount: 滚动幅度，默认 120（一个滚轮单位）
    """
    with lock:
        x = int(x)
        y = int(y)

        # wParam 高16位是滚动量，低16位是键盘状态（一般为 0）
        w_param = (scroll_amount << 16)
        # lParam 高16位是Y坐标，低16位是X坐标
        l_param = (y << 16) | x
        # 同步发送鼠标滚轮事件
        win32api.SendMessage(hwnd, win32con.WM_MOUSEWHEEL, w_param, l_param)


# 左键点击指定 hwnd
def mouse_left_click_hwnd(hwnd, x, y):
    with lock:
        x = int(x)
        y = int(y)
        win32api.SendMessage(hwnd, 0x0201, 1, (y << 16) | x)
        time.sleep(0.02)
        win32api.SendMessage(hwnd, 0x0202, 0, (y << 16) | x)


# 右键点击指定 hwnd
def mouse_right_click_hwnd(hwnd, x, y):
    with lock:
        x = int(x)
        y = int(y)
        win32api.SendMessage(hwnd, 0x0204, 1, (y << 16) | x)
        win32api.SendMessage(hwnd, 0x0205, 0, (y << 16) | x)


# 中键点击指定 hwnd
def mouse_middle_click_hwnd(hwnd, x, y):
    with lock:
        x = int(x)
        y = int(y)
        l_param = (y << 16) | x
        ctypes.windll.user32.PostMessageW(hwnd, 0x0207, win32con.MK_MBUTTON, l_param)
        ctypes.windll.user32.PostMessageW(hwnd, 0x0208, 0, l_param)


# hwnd 是否激活
def is_window_foreground(hwnd):
    foreground_hwnd = ctypes.windll.user32.GetForegroundWindow()
    return hwnd == foreground_hwnd


# activate_window 将窗口激活
def activate_window(hwnd):
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.02)


# 窗口状态
def window_state_by_text(hwnd):
    res = ""
    if win32gui.GetForegroundWindow() == hwnd:
        res = f"激活：YES"
    else:
        res = f"激活：NO"
    if not win32gui.IsWindowVisible(hwnd):
        res = f"{res} - 隐藏：YES"
    else:
        res = f"{res} - 隐藏：NO"
    return res


# 获取桌面窗口句柄
def get_desktop_window_handle():
    return windll.user32.GetDesktopWindow()


# 当前活动的 hwnd
def GetForegroundWindow():
    return win32gui.GetForegroundWindow()


# 获取窗口句柄（最前面那个）
def get_window_handle(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        print(f"无法找到窗口 '{window_name}'")
        return None
    return hwnd


def get_hwnd_name(hwnd):
    title = win32gui.GetWindowText(hwnd)
    return title


# 获取所有符合窗口名称的窗口句柄
def get_all_window_handles_by_name(window_name):
    window_handles = []

    def enum_windows_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):  # 只匹配可见窗口
            title = win32gui.GetWindowText(hwnd)
            # print(title)
            if window_name in title:
                window_handles.append(hwnd)

    # 遍历所有窗口
    win32gui.EnumWindows(enum_windows_callback, None)
    return window_handles


def get_all_window_handle_title_in_name(window_name):
    window_handles = []
    handles_title = []

    def enum_windows_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):  # 只匹配可见窗口
            title = win32gui.GetWindowText(hwnd)
            # print(title)
            if window_name in title:
                window_handles.append(hwnd)
                handles_title.append(title)

    # 遍历所有窗口
    win32gui.EnumWindows(enum_windows_callback, None)
    return window_handles, handles_title


def send_key_to_all_windows(window_name, key_to_send):
    window_handles = get_all_window_handles_by_name(window_name)
    if window_handles:
        for hwnd in window_handles:
            print(f"发送按键 {key_to_send} 到窗口句柄: {hwnd}")
            send_key_to_window(hwnd, key_to_send)
    else:
        print(f"未找到窗口名称包含 '{window_name}' 的窗口")


def send_key_to_window(hwnd, key_name, duration=0.02):
    if isinstance(key_name, str):
        key_name = key_map.get(key_name.lower())
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, key_name, 0)
    time.sleep(duration)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, key_name, 0)


# 后台发送按键消息
def send_key_to_window_frequency(hwnd, key_name, frequency=1):
    if isinstance(key_name, str):
        key_name = key_map.get(key_name.lower())
    print(f"{hwnd}, {key_name}, {frequency}")
    for _ in range(frequency):
        win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, key_name, 0)
        time.sleep(0.01)
        win32api.SendMessage(hwnd, win32con.WM_KEYUP, key_name, 0)


def type_in_window_by_hwnd(hwnd, text):
    for char in text:
        # 获取字符的虚拟键码
        vk_code = win32api.VkKeyScan(char)

        # 发送按键消息
        win32api.SendMessage(hwnd, win32con.WM_CHAR, vk_code, 0)
        time.sleep(0.05)  # 模拟按键延迟


def type_in_window_text(text):
    pyautogui.typewrite(text, interval=0.05)  # 模拟输入


def press(key):
    pyautogui.press(key)


def press_enter():
    pyautogui.press('enter')  # 模拟按下回车键


def press_backspace(count=1):
    print(f"press_backspace={count}")
    for i in range(count):
        time.sleep(0.01)
        pyautogui.press('backspace')


# 粘贴板复制文本
def paste_text(text):
    # 将文本放入剪贴板
    pyperclip.copy(text)

    # 模拟 Ctrl + V 粘贴
    pyautogui.hotkey('ctrl', 'v')


# send_key 前台按键
def send_key(key_name, frequency=1):
    key_code = key_map.get(key_name.lower())
    for i in range(frequency):
        win32api.keybd_event(key_code, 0, 0, 0)
        time.sleep(0.015)
        win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)


# 前台按键，持续 durationn s
def send_press_key(key_name, duration=1):
    key_code = key_map.get(key_name.lower())
    win32api.keybd_event(key_code, 0, 0, 0)
    time.sleep(duration)
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)


def SendMessageWFrequency(hwnd, key_name, frequency=1):
    with lock:
        if isinstance(key_name, str):
            key_name = key_map.get(key_name.lower())
        for _ in range(frequency):
            # ctypes.windll.user32.SendMessageW(hwnd,  win32con.WM_KEYDOWN, key_name, 0)
            # time.sleep(0.02)
            # ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_KEYUP, key_name, 0)
            ctypes.windll.user32.PostMessageW(hwnd,  win32con.WM_KEYDOWN, key_name, 0)
            time.sleep(0.02)
            ctypes.windll.user32.PostMessageW(hwnd, win32con.WM_KEYUP, key_name, 0)


def send_text_to_hwnd(hwnd, text):
    with lock:
        for char in text:
            time.sleep(0.005)  # 调整延迟时间，模拟自然输入效果
            # 将字符转换为 Unicode 编码
            char_code = ord(char)
            # 发送 WM_CHAR 消息，逐个输入字符
            ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_CHAR, char_code, 0)


VK_NUMPAD2 = 0x62  # 小键盘上的 2 键
VK_NUMPAD4 = 0x64  # 小键盘上的 4 键
VK_NUMPAD5 = 0x65  # 小键盘上的 5 键
VK_NUMPAD6 = 0x66  # 小键盘上的 6 键
VK_NUMPAD8 = 0x68  # 小键盘上的 8 键

def SendMessageW_Extended_KEY(hwnd, key_code, duration=0.05):
    with lock:
        # 构造 WM_KEYDOWN 的 lParam 参数
        lParam_keydown = (1 | (0x50 << 16) | (1 << 24))  # 扫描码为 0x50，设置扩展键标志 (1 << 24)

        # 发送小键盘上的 2 键的 WM_KEYDOWN 消息
        ctypes.windll.user32.PostMessageW(hwnd, 0x0100, key_code, lParam_keydown)
        time.sleep(duration)  # 延迟模拟自然按键时间

        # 构造 WM_KEYUP 的 lParam 参数
        lParam_keyup = (1 | (0x50 << 16) | (1 << 24) | (1 << 30) | (1 << 31))

        # 发送小键盘上的 2 键的 WM_KEYUP 消息
        ctypes.windll.user32.PostMessageW(hwnd, 0x0101, key_code, lParam_keyup)


def send_key_to_window_enter(hwnd):
    SendMessageWFrequency(hwnd, 0x0D)


def send_key_to_window_backspace(hwnd, frequency=1):
    SendMessageWFrequency(hwnd, 0x08, frequency)


if __name__ == "__main__":
    pass
    # desktop_handle = get_desktop_window_handle()
    # print(f"桌面窗口句柄: {desktop_handle}")
    # window_name = "夏禹剑 - 刀剑2"
    # hwnd = get_window_handle(window_name)
    # ss = get_screen_scale(hwnd)
    # print(ss)
    # cp = calculate_physical_pixels(100, ss)
    # print(cp)
    # print(calculate_offset(100))
