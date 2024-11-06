from dao2 import win_tool
import time

window_name = "夏禹剑 - 刀剑2"
hwnd = win_tool.get_window_handle(window_name)

text = "test - 群开竞技赛"

win_tool.send_key_to_window_enter(hwnd)
time.sleep(0.02)
win_tool.send_text_to_hwnd(hwnd, text)
time.sleep(0.02)
win_tool.send_key_to_window_enter(hwnd)
time.sleep(0.02)
