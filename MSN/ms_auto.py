import threading
import time
import keyboard
from MSN import win_tool
import msn
import py_tool
import log3

lock = threading.Lock()

is_running_auto_attack = False
is_running_auto_collect = False
is_running_auto_mp = False
is_running_auto_hp = False


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
        time.sleep(0.1)
        if not win_tool.is_window_foreground(hwnd):
            continue
        counter += 1

        if counter % 5 == 0:
            keyboard.press_and_release('2')
        else:
            keyboard.press_and_release('1')
        time.sleep(py_tool.rand_min_float(0.2))

        if counter % 10 == 0:
            direction = not direction
        if direction:
            keyboard.press("left")
            time.sleep(py_tool.rand_min_float(0.7))
            keyboard.release("left")
        else:
            keyboard.press("right")
            time.sleep(py_tool.rand_min_float(0.7))
            keyboard.release("right")


def run_auto_collect(hwnd):
    log3.logger.info("run_auto_collect")
    global is_running_auto_collect
    while is_running_auto_collect:
        time.sleep(py_tool.rand_min_float(0.05))
        if not win_tool.is_window_foreground(hwnd):
            continue
        keyboard.press_and_release('z')
        time.sleep(py_tool.rand_min_float(0.05))


def run_auto_mp(hwnd):
    log3.logger.info("run_auto_mp")
    global is_running_auto_mp
    while is_running_auto_mp:
        time.sleep(0.5)
        if not win_tool.is_window_foreground(hwnd):
            continue
        if None is msn.is_mp(hwnd):
            # 没蓝 吃
            keyboard.press_and_release('q')


def run_auto_hp(hwnd):
    log3.logger.info("run_auto_hp")
    global is_running_auto_hp
    while is_running_auto_hp:
        time.sleep(0.3)
        if not win_tool.is_window_foreground(hwnd):
            continue
        if None is msn.is_hp(hwnd):
            keyboard.press_and_release('w')
