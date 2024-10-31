import time

import win32gui
import win32con
import win32api
import ctypes
import pyautogui
import pyperclip
import os
import sys
from ctypes import windll


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
    # 如果传递了 hwnd，获取该窗口的 DPI，否则获取主显示器 DPI
    hdc = ctypes.windll.user32.GetDC(hwnd) if hwnd else ctypes.windll.user32.GetDC(0)
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX, 88是水平DPI
    ctypes.windll.user32.ReleaseDC(hwnd, hdc)

    # 计算缩放比例
    scale_factor = dpi / 96  # 96 DPI 是标准缩放（100%）
    return scale_factor

# 定义鼠标事件的常量
MOUSEEVENTF_MOVE = 0x0001  # 鼠标移动
MOUSEEVENTF_LEFTDOWN = 0x0002  # 鼠标左键按下
MOUSEEVENTF_LEFTUP = 0x0004  # 鼠标左键抬起
MOUSEEVENTF_ABSOLUTE = 0x8000  # 绝对坐标
MOUSEEVENTF_RIGHTDOWN = 0x0008  # 右键按下
MOUSEEVENTF_RIGHTUP = 0x0010    # 右键抬起


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
    time.sleep(0.05)


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
    abs_x, abs_y = absolute_coords(x, y)

    # 模拟鼠标移动到指定位置
    mi_move = MOUSEINPUT(dx=abs_x, dy=abs_y, mouseData=0, dwFlags=MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, time=0,
                         dwExtraInfo=None)
    input_move = INPUT(type=0, mi=mi_move)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_move), ctypes.sizeof(input_move))
    time.sleep(0.1)
    # 模拟鼠标左键按下
    mi_down = MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_LEFTDOWN, time=0, dwExtraInfo=None)
    input_down = INPUT(type=0, mi=mi_down)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_down), ctypes.sizeof(input_down))

    # 模拟鼠标左键抬起
    mi_up = MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_LEFTUP, time=0, dwExtraInfo=None)
    input_up = INPUT(type=0, mi=mi_up)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_up), ctypes.sizeof(input_up))


def send_input_mouse_right_click(x, y):
    move_mouse(x, y)
    time.sleep(0.05)
    mouse_right_click()


def mouse_right_click():
    mi_down = MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_RIGHTDOWN, time=0, dwExtraInfo=None)
    input_down = INPUT(type=0, mi=mi_down)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_down), ctypes.sizeof(input_down))

    mi_up = MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_RIGHTUP, time=0, dwExtraInfo=None)
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


# activate_window 将窗口设置为前台
def activate_window(hwnd):
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.02)


# 获取窗口句柄的函数
def get_window_handle(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        print(f"无法找到窗口 '{window_name}'")
        return None
    return hwnd


# 获取屏幕宽度和高度
def get_win_w_h():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)  # 参数 0 表示屏幕宽度
    screen_height = user32.GetSystemMetrics(1)  # 参数 1 表示屏幕高度
    return screen_width, screen_height


# 获取所有符合窗口名称的窗口句柄，并返回存储句柄的数组
def get_all_window_handles_by_name(window_name):
    """
    获取所有符合窗口名称的窗口句柄，并返回存储句柄的数组

    参数:
    - window_name: 需要匹配的窗口名称

    返回:
    - 符合窗口名称的窗口句柄数组
    """
    window_handles = []

    def enum_windows_callback(hwnd, extra):
        # 获取窗口标题
        if win32gui.IsWindowVisible(hwnd):  # 只匹配可见窗口
            title = win32gui.GetWindowText(hwnd)
            if window_name in title:
                window_handles.append(hwnd)

    # 遍历所有窗口
    win32gui.EnumWindows(enum_windows_callback, None)

    return window_handles


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
    for i in range(frequency):
        win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, key_name, 0)
        time.sleep(0.015)
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
def send_press_key(key_name, durationn=1):
    key_code = key_map.get(key_name.lower())
    win32api.keybd_event(key_code, 0, 0, 0)
    time.sleep(durationn)
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)


# 向上滚动鼠标滚轮
def scroll_mouse_up(amount):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, amount, 0)


# 向下滚动鼠标滚轮
def scroll_mouse_down(amount):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -amount, 0)


def get_desktop_window_handle():
    # 调用 Windows API 获取桌面窗口句柄
    return windll.user32.GetDesktopWindow()


if __name__ == "__main__":
    desktop_handle = get_desktop_window_handle()
    print(f"桌面窗口句柄: {desktop_handle}")