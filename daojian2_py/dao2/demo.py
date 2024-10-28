import time

import bg_find_pic
import bg_find_pic_area
import win_tool
import dao2_common

if __name__ == "__main__":
    w, h = win_tool.get_win_w_h()
    print(f"w={w},h={h}")

    window_name = "夏禹剑 - 刀剑2"
    hwnd = win_tool.get_window_handle(window_name)

    time.sleep(1)
    win_tool.activate_window(hwnd)
    # win_tool.send_key("w", 3)
    # time.sleep(0.6)
    # win_tool.send_key("E", 1)
    dao2_common.close_6_oclock_dialog(hwnd)


