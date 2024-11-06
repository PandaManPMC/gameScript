import ctypes
import win32api
import win32gui
import win32con
import time

from dao2 import win_tool


# 鼠标左键
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202


def send_mouse_left_click(hwnd, x, y):
    x = int(x)
    y = int(y)
    print(f"点击 x={x} y={y}")

    l_param = (y << 16) | x
    print(f"{l_param}")

    ctypes.windll.user32.PostMessageW(hwnd, WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    time.sleep(0.02)
    ctypes.windll.user32.PostMessageW(hwnd, WM_LBUTTONUP, 0, l_param)


# 鼠标右键
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205


def send_mouse_right_click(hwnd, x, y):
    l_param = (y << 16) | x
    ctypes.windll.user32.PostMessageW(hwnd, WM_RBUTTONDOWN, win32con.MK_RBUTTON, l_param)
    ctypes.windll.user32.PostMessageW(hwnd, WM_RBUTTONUP, 0, l_param)
    print(f"已向句柄 {hwnd} 发送右键点击事件")


# 鼠标中键
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208


def send_mouse_middle_click(hwnd, x, y):
    l_param = (y << 16) | x
    ctypes.windll.user32.PostMessageW(hwnd, WM_MBUTTONDOWN, win32con.MK_MBUTTON, l_param)
    ctypes.windll.user32.PostMessageW(hwnd, WM_MBUTTONUP, 0, l_param)


# 定义鼠标移动消息
WM_MOUSEMOVE = 0x0200

def move_mouse_to(hwnd, x, y):
    """
    向指定窗口句柄发送鼠标移动事件
    :param hwnd: 目标窗口的句柄
    :param x: 移动到的 x 坐标（相对于窗口）
    :param y: 移动到的 y 坐标（相对于窗口）
    """
    l_param = (y << 16) | x
    ctypes.windll.user32.PostMessageW(hwnd, WM_MOUSEMOVE, 0, l_param)


# 定义鼠标滚轮消息
WM_MOUSEWHEEL = 0x020A

def scroll_mouse_wheel_at(hwnd, x, y, scroll_amount=120):
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


def send_text_to_hwnd(hwnd, text):
    for char in text:
        time.sleep(0.05)  # 调整延迟时间，模拟自然输入效果
        # 将字符转换为 Unicode 编码
        char_code = ord(char)
        # 发送 WM_CHAR 消息，逐个输入字符
        ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_CHAR, char_code, 0)


# 定义按键消息
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

def send_key_to_hwnd(hwnd, key_code):
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYDOWN, key_code, 0)
    time.sleep(0.05)  # 延迟以模拟自然按键时间
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYUP, key_code, 0)
    print(f"已向句柄 {hwnd} 发送按键: {key_code}")


# 定义按键消息
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101


def send_key_to_inactive_hwnd(hwnd, key_code):
    """
    向不激活的窗口句柄发送按键消息
    :param hwnd: 目标窗口的句柄
    :param key_code: 要发送的按键虚拟键码（例如 Enter 键为 0x0D）
    """
    # 发送按键按下事件
    ctypes.windll.user32.SendMessageW(hwnd, WM_KEYDOWN, key_code, 0)
    time.sleep(0.01)  # 模拟按键按住的效果

    # 发送按键松开事件
    ctypes.windll.user32.SendMessageW(hwnd, WM_KEYUP, key_code, 0)
    print(f"已向句柄 {hwnd} 发送按键: {key_code}")


# 获取指定窗口句柄（假设窗口标题已知）
window_name = "夏禹剑 - 刀剑2"
hwnd = win_tool.get_window_handle(window_name)

print(hwnd)
if hwnd:
    # 1356 y=554
    # send_mouse_left_click(hwnd, x=1226, y=546)  # 发送点击到窗口客户区 (100, 100) 位置
    # send_mouse_right_click(hwnd, x=1127, y=527)
    send_mouse_middle_click(hwnd,  x=158, y=860)
    # move_mouse_to(hwnd, 158, 860)
    # time.sleep(2)
    # move_mouse_to(hwnd, 2053, 46)
    # scroll_mouse_wheel_at(hwnd, 2360, 984, -240)


    # win_tool.send_key_to_window_backspace(hwnd, 20)
    # send_text_to_hwnd(hwnd, "646,849")
    # time.sleep(1)


    # send_text_to_hwnd(hwnd, "中文3")
    # send_text_to_hwnd(hwnd, "飞流直下三千尺 疑是银河落九天")
    # while True:
    #     send_key_to_inactive_hwnd(hwnd, 0x77)
    #     time.sleep(0.2)
    # send_key_to_hwnd(hwnd, 0x0D)
    # win_tool.send_key_to_window_enter(hwnd)
    # WM_KEYDOWN = 0x0100
    # WM_KEYUP = 0x0101
    # VK_BACKSPACE = 0x08
    #
    # for _ in range(20):
    #     ctypes.windll.user32.PostMessageW(hwnd, WM_KEYDOWN, VK_BACKSPACE, 0)
    #     time.sleep(0.01)
    #     ctypes.windll.user32.PostMessageW(hwnd, WM_KEYUP, VK_BACKSPACE, 0)

else:
    print("未找到指定窗口")
