import ctypes
import time
from dao2 import win_tool

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
VK_ENTER = 0x0D


def send_enter_with_multiple_keydown(hwnd):
    lParam_keydown = (1 | (0x1C << 16))

    # 发送多次 WM_KEYDOWN 消息来模拟按住状态
    for _ in range(3):
        ctypes.windll.user32.PostMessageW(hwnd, WM_KEYDOWN, VK_ENTER, lParam_keydown)
        time.sleep(0.1)  # 短暂延迟，模拟按住效果

    # 发送 WM_KEYUP 消息
    lParam_keyup = (1 | (0x1C << 16) | (1 << 30) | (1 << 31))
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYUP, VK_ENTER, lParam_keyup)


# 获取指定窗口句柄（假设窗口标题已知）
window_name = "夏禹剑 - 刀剑2"
hwnd = win_tool.get_window_handle(window_name)

print(hwnd)
if hwnd:
    # send_enter_with_multiple_keydown(hwnd)
    # win_tool.send_text_to_hwnd(hwnd, "1005,1047")
    # time.sleep(0.1)
    # win_tool.send_key_to_window_enter(hwnd)
    win_tool.SendMessageW_Extended_KEY(hwnd, win_tool.VK_NUMPAD5)
else:
    print("未找到指定窗口")