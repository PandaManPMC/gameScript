import time

import cv2
import threading
import psutil
import os
import gc
import log3

MAX_MEMORY_LIMIT = 500 * 1024 * 1024  # 500 MB


def check_memory():
    process = psutil.Process(os.getpid())
    mem_usage = process.memory_info().rss
    if mem_usage > MAX_MEMORY_LIMIT:
        gc.collect()  # 进行垃圾回收


def start_release_job():
    t = threading.Thread(target=release, args=(), daemon=True)
    t.start()


def release():
    while True:
        time.sleep(60)
        log3.logger.info(f"app release MAX_MEMORY_LIMIT={MAX_MEMORY_LIMIT}")
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        check_memory()