import win_tool
import threading
import time
import traceback
from tkinter import messagebox
import log3

# 自动拾取：控制线程是否继续执行
runningCollect = False
lockCollect = threading.Lock()


def collect(window_name):
    while runningCollect:
        win_tool.send_key_to_all_windows(window_name, "z")
        time.sleep(0.5)