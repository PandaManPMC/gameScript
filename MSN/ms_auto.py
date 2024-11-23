import threading
import time
import keyboard
from MSN import win_tool
import msn

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
    counter = 0
    direction = False
    while is_running_auto_attack:
        time.sleep(0.3)
        if not win_tool.is_window_foreground(hwnd):
            continue
        keyboard.press_and_release('1')
        counter += 1

        if counter % 5 == 0:
            if None is msn.is_mp(hwnd):
                # 没蓝 吃
                keyboard.press_and_release('q')

        if counter % 30 == 0:
            direction = not direction
        if direction:
            keyboard.press("left")
            time.sleep(0.3)
            keyboard.release("left")
        else:
            keyboard.press("right")
            time.sleep(0.3)
            keyboard.release("right")


def run_auto_collect(hwnd):
    with lock:
        # 开启子线程
        t = threading.Thread(target=auto_collect, args=(hwnd,), daemon=True)
        t.start()


def auto_collect(hwnd):
    # win_tool.activate_window(hwnd)
    global is_running_auto_collect
    while is_running_auto_collect:
        time.sleep(0.2)
        if not win_tool.is_window_foreground(hwnd):
            continue
        keyboard.press_and_release('z')
        time.sleep(0.1)
