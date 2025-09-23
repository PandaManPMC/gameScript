import time

from . import win_tool
import threading


is_run_mouse_right_click = False
lock_run_mouse_right_click = threading.Lock()


def while_mouse_right_click(interval):
    time.sleep(0.1)
    global is_run_mouse_right_click
    while is_run_mouse_right_click:
        win_tool.click_right_current_position()
        time.sleep(interval)


is_run_mouse_left_click = False
lock_run_mouse_left_click = threading.Lock()


def while_mouse_left_click(interval):
    time.sleep(0.1)
    global is_run_mouse_left_click
    while is_run_mouse_left_click:
        win_tool.click_left_current_position()
        time.sleep(interval)