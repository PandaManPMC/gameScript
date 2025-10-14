import time

import gamelib

is_run_chrome_refresh = False


# run_chrome_refresh 浏览器崩溃刷新
def run_chrome_refresh(hwnd):
    global is_run_chrome_refresh
    w,h = gamelib.win_tool.get_win_w_h()
    while is_run_chrome_refresh:
        time.sleep(5)
        # 找强化按钮
        xy = gamelib.bg_find_pic_area.find_image(hwnd, "img/qianghua_btn.bmp", int(w * 0.15), int(h * 0.2), int(w * 0.8), int(h * 0.9), 0.8)
        if None is xy:
            gamelib.log3.console(hwnd + " 未找到崩溃图标")
            time.sleep(30)
            continue
        key_code = gamelib.win_tool.key_map.get("f5")
        gamelib.win_tool.send_key_to_window(hwnd, key_code)
        time.sleep(15)
        gamelib.win_tool.send_key_to_window(hwnd, gamelib.win_tool.key_map.get("z"))
