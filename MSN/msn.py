import app_const
import win_tool
import bg_find_pic_area


# 蓝是否足够
def is_mp(hwnd):
    x_of = int(app_const.screen_w * 0.4)
    y_of = int(app_const.screen_h * 0.85)
    bo_w = int(app_const.screen_w * 0.6)
    bo_h = app_const.screen_h
    return bg_find_pic_area.find_image(hwnd, win_tool.resource_path("img/mp.bmp"), x_of, y_of, bo_w, bo_h, 0.8)


