from dao2 import win_tool
from dao2 import dao2_common
import time

window_name = "夏禹剑 - 刀剑2"
hwnd = win_tool.get_window_handle(window_name)

for _ in range(5):
    dh_xy = dao2_common.find_da_huang_list(hwnd)
    if None is dh_xy:
        print("没找到大黄")
        # 大黄挖没了，打断
        break
    win_tool.send_mouse_left_click(hwnd, dh_xy[0], dh_xy[1]+8)
    time.sleep(6)



