import time
import keyboard

from MSN import win_tool


# 示例用法
if __name__ == "__main__":
    window_name = "MapleStory N"
    window_handles = win_tool.get_all_window_handles_by_name(window_name)
    hwnd = window_handles[0]
    win_tool.activate_window(hwnd)

    while True:
        # send_key_1()  # 发送数字 '1'1
        time.sleep(0.3)
        keyboard.press_and_release('1')


