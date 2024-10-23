import time

import bg_find_pic
import bg_find_pic_area
import win_tool

if __name__ == "__main__":
    w, h = win_tool.get_win_w_h()
    print(f"w={w},h={h}")

    window_name = "夏禹剑 - 刀剑2"  # 替换为你的游戏窗口名称
    #template_img_path = "./img/banghuishizhe.bmp"  # 替换为你要匹配的模板图片路径
    template_img_path = "./img/daohang_shurukuan.bmp"  # 替换为你要匹配的模板图片路径

    hwnd = win_tool.get_window_handle(window_name)

    match_location = bg_find_pic.find_image_in_window(hwnd, template_img_path, 0.7)
    if match_location:
        print(f"图像匹配成功，坐标: {match_location}")
    else:
        print("图像匹配失败")

    # 屏幕缩放后的坐标获取
    scale = win_tool.get_screen_scale()

    x, y = match_location
    print(f"scale={scale} , x={scale * x}, y={scale * y}")

    # 设置截图范围，x_offset, y_offset, capture_width, capture_height
    match_location = bg_find_pic_area.find_image_in_window(hwnd, template_img_path, x_offset=400, y_offset=300, capture_width=2560 - 500,
                                          capture_height=1440 - 400)
    if match_location:
        print(f"区域 图像匹配成功，坐标: {match_location}")
    else:
        print("区域 图像匹配失败")

    x, y = match_location
    x = scale * (x + 400) + 20
    y = scale * (y + 300) + 10
    print(f"scale={scale} , x={x}, y={y}")

    hwnd = win_tool.get_window_handle(window_name)
    # bg_click_left.send_mouse_click(hwnd, scale * (x+400) + 15, scale * (y+300) + 15)

    win_tool.activate_window(hwnd)
    time.sleep(0.5)
    win_tool.send_input_mouse_left_click(x, y)

