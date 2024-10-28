import win_tool
import threading
import time
import dao2_common
import traceback
from tkinter import messagebox

w, h = win_tool.get_win_w_h()

is_run = False
lock = threading.Lock()


def start_arena(hwnd_array):
    global is_run
    with lock:
        if is_run:
            t = threading.Thread(target=arena, args=(hwnd_array,), daemon=True)
            t.start()


def arena(hwnd_array):
    global is_run
    while is_run:
        for hwnd in hwnd_array:
            win_tool.activate_window(hwnd)
            time.sleep(0.3)
