import threading
import time
import keyboard
from MSN import win_tool

lock = threading.Lock()

is_running_auto_attack = False
is_running_auto_collect = False


def run_auto_attack(hwnd):
    with lock:
        # 开启子线程
        t = threading.Thread(target=auto_attack, args=(hwnd,), daemon=True)
        t.start()


def auto_attack(hwnd):
    win_tool.activate_window(hwnd)
    global is_running_auto_attack
    while is_running_auto_attack:
        time.sleep(0.3)
        if not win_tool.is_window_foreground(hwnd):
            continue
        keyboard.press_and_release('1')
        time.sleep(0.3)


def run_auto_collect(hwnd):
    with lock:
        # 开启子线程
        t = threading.Thread(target=auto_collect, args=(hwnd,), daemon=True)
        t.start()


def auto_collect(hwnd):
    win_tool.activate_window(hwnd)
    global is_running_auto_collect
    while is_running_auto_collect:
        time.sleep(0.2)
        if not win_tool.is_window_foreground(hwnd):
            continue
        keyboard.press_and_release('z')
        time.sleep(0.1)
