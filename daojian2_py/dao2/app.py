import time

import threading
import psutil
import os
import gc
import log3
import dao2_common

MAX_MEMORY_LIMIT = 500 * 1024 * 1024  # 500 MB


def check_memory():
    process = psutil.Process(os.getpid())
    mem_usage = process.memory_info().rss
    if mem_usage > MAX_MEMORY_LIMIT:
        gc.collect()  # 进行垃圾回收


def start_release_job():
    t = threading.Thread(target=release, args=(), daemon=True)
    t.start()


is_run_release = True


def release():
    while is_run_release:
        time.sleep(360)
        log3.logger.info(f"app release MAX_MEMORY_LIMIT={MAX_MEMORY_LIMIT}")
        # cv2.destroyAllWindows()
        check_memory()


is_run_active_game_window = True


# 激活 window 避免暂离
def active_game_window(hwnd):
    global is_run_active_game_window
    while is_run_active_game_window:
        time.sleep(1)
        dao2_common.activity_window(hwnd)
        log3.logger.info("防止暂离 active_game_window")
        time.sleep(170)
