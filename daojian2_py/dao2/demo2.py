import time

import win_tool

if __name__ == "__main__":
    window_name = "刀剑2"  # 替换为你想要匹配的窗口名称
    handles = win_tool.get_all_window_handles_by_name(window_name)

    if handles:
        print(f"找到的窗口句柄: {handles}")
    else:
        print("未找到符合条件的窗口")

    for hwnd in handles:
        try:
            print(f"激活窗口句柄: {hwnd}")
            win_tool.activate_window(hwnd)
            time.sleep(3)  # 延迟
        except Exception as e:
            print(f"无法激活窗口句柄: {hwnd}, 错误: {e}")


