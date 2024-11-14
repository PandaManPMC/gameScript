import win_tool
import dao2_common
import time


w,h = win_tool.get_win_w_h()

window_name = "夏禹剑 - 刀剑2"
hwnd = win_tool.get_window_handle(window_name)

win_tool.send_key_to_window_frequency(hwnd, "1", 1)
time.sleep(1.3)
win_tool.send_key_to_window_frequency(hwnd, "2", 1)
time.sleep(0.7)

win_tool.send_key_to_window_frequency(hwnd, "e", 1)
time.sleep(4.5)

# xy = dao2_common.find_pic(hwnd, "img/nununu.bmp", int(0.25*w), int(0.4*h), int(w * 0.75), int(h * 0.98), 0.8)
# print(xy)
#
# xy = dao2_common.find_pic(hwnd, "img/2jizongzi.bmp", int(0.25*w), int(0.4*h), int(w * 0.75), int(h * 0.98), 0.8)
# print(xy)
# eat_zong_zi(hwnd)

# win_tool.send_mouse_left_click(hwnd, 1244, 505)
# time.sleep(0.1)
# win_tool.send_mouse_left_click(hwnd, 1244, 505)

# win_tool.send_mouse_left_click(hwnd, 1225 + 4, 397 + 8)

# dao2_common.camera_top(hwnd)
# time.sleep(1)
#
# for _ in range(3):
#     xy = dao2_common.find_gan_cao_list(hwnd)
#
#     if None is not xy:
#         time.sleep(0.06)
#         dao2_common.open_navigation_and_click(hwnd)
#         time.sleep(0.06)
#         win_tool.send_mouse_left_click(hwnd, xy[0] + 4, xy[1] + 8)
#         time.sleep(0.06)
#         win_tool.send_mouse_left_click(hwnd, xy[0] + 4, xy[1] + 8)
#         time.sleep(5.7)

# dao2_common.open_navigation_and_click(hwnd)
#
# c = 1
# while c < 7:
#
#     dh_xy = dao2_common.find_da_huang_list(hwnd)
#     if None is dh_xy:
#         print("没找到大黄")
#         # 大黄挖没了，打断
#         break
#     # win_tool.move_mouse_to(hwnd, dh_xy[0]+4, dh_xy[1]+8)
#     win_tool.send_mouse_left_click(hwnd, dh_xy[0]+4, dh_xy[1]+8)
#     print(c)
#     if 0 != c and c % 2 == 0:
#         time.sleep(6)
#         # win_tool.send_mouse_right_click(hwnd, dh_xy[0]+4, dh_xy[1]+8)
#         dao2_common.open_navigation_and_click(hwnd)
#     else:
#         time.sleep(0.2)
#     c += 1


# dao2_common.navigation_x_y(hwnd, "1069,1240")



