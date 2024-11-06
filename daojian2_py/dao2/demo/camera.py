from dao2 import dao2_common
from dao2 import win_tool


window_name = "夏禹剑 - 刀剑2"
hwnd = win_tool.get_window_handle(window_name)

dao2_common.camera_top(hwnd)