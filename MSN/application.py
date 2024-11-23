import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import keyboard
from tkinter import messagebox
import ms_auto
import win_tool
from MSN import log3, app_const, ms_quick

window_name = "MapleStory N"

# 窗口置顶
topmost = False

# 窗口句柄
hwnd_array = []

hwnd_array_str = []

# 全局UI控制锁
LOCK_GLOBAL_UI = threading.Lock()


def root_click(event):
    # 在点击其他地方时，将焦点移出输入框
    # input_entry.focus_out()
    # num_entry.focus_out()
    # input_hwnd_send_key.focus_out()
    # mu_ye_entry.focus_out()
    # if event.widget != input_entry \
    #         and event.widget != input_entry \
    #         and event.widget != input_hwnd_send_key \
    #         and event.widget != mu_ye_entry \
    #         and event.widget != input_say_time \
    #         and event.widget != input_say_content:  # 只有点击其他地方才失去焦点

    root.focus_set()


def validate_float(value_if_allowed):
    if value_if_allowed == "":
        return True
    try:
        float(value_if_allowed)
        return True
    except ValueError:
        return False


def on_closing():
    log3.console("关闭所有线程，确保程序完全退出")
    ms_quick.runningCollect = False
    ms_auto.is_running_auto_attack = False
    ms_auto.is_running_auto_collect = False
    root.destroy()


# stop_all_script 停止所有脚本
def stop_all_script(event=None):
    global current_live_script_name
    log3.console("stop_all_script")
    ms_auto.is_running_auto_attack = False
    ms_auto.is_running_auto_collect = False
    ms_quick.runningCollect = False
    # messagebox.showwarning("提示", "所有脚本已停止")


def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def toggle_topmost():
    global topmost
    topmost = not topmost
    if topmost:
        root.attributes('-topmost', True)
        btn_topmost.config(text="取消置顶")
        log3.console("窗口已置顶")
    else:
        root.attributes('-topmost', False)
        btn_topmost.config(text="窗口置顶")
        log3.console("取消窗口置顶")


def active_window():
    selected_index = combobox.current()  # 获取选择框的当前下标
    log3.console(f"选择的下标：{selected_index}")
    hwnd = hwnd_array[selected_index]
    win_tool.activate_window(hwnd)


def toggle_collect(event=None):
    with LOCK_GLOBAL_UI:
        ms_quick.runningCollect = not ms_quick.runningCollect
        if ms_quick.runningCollect:
            btn_collect.config(bg="red")
            t = threading.Thread(target=ms_quick.collect, args=(window_name,), daemon=True)
            t.start()
        else:
            btn_collect.config(bg="white")


def auto_attack(event=None):
    selected_index = combobox.current()
    hwnd = hwnd_array[selected_index]

    with LOCK_GLOBAL_UI:
        ms_auto.is_running_auto_attack = not ms_auto.is_running_auto_attack
        if ms_auto.is_running_auto_attack:
            btn_auto_attack.config(bg="red")
            t = threading.Thread(target=ms_auto.run_auto_attack, args=(hwnd,), daemon=True)
            t.start()
        else:
            btn_auto_attack.config(bg="white")


def auto_collect(event=None):
    hwnd = hwnd_array[combobox.current()]
    with LOCK_GLOBAL_UI:
        ms_auto.is_running_auto_collect = not ms_auto.is_running_auto_collect
        if ms_auto.is_running_auto_collect:
            btn_auto_collect.config(bg="red")
            t = threading.Thread(target=ms_auto.run_auto_collect, args=(hwnd,), daemon=True)
            t.start()
        else:
            btn_auto_collect.config(bg="white")


if __name__ == "__main__":

    # 创建 Tkinter GUI
    root = tk.Tk()
    root.title(app_const.APP_NAME)
    root.geometry(app_const.WINDOW_GEOMETRY)  # 调整窗口大小

    root.attributes('-alpha', 0.96)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 创建一个画布和滚动条
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 布局滚动条和画布
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # 绑定鼠标滚轮事件
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # frame 第一排按钮
    label = tk.Label(scrollable_frame, text=f"严正声明：\n",
                     fg="red", anchor='w', justify='left')
    label.pack(fill='x', pady=1)

    frame = tk.Frame(scrollable_frame)
    frame.pack(pady=10, anchor='w', fill='x')

    btn_topmost = tk.Button(frame, text="窗口置顶", width=14, height=1, command=toggle_topmost)
    btn_topmost.pack(side=tk.LEFT, padx=10)

    btn_collect = tk.Button(frame, text="自动拾取", width=14, height=1, command=toggle_collect)
    btn_collect.pack(side=tk.LEFT, padx=10)

    # 窗口句柄选择, 以及之后的单控选项
    selection_frame = tk.Frame(scrollable_frame)
    selection_frame.pack(pady=20, side=tk.TOP, fill="x", anchor="w")

    hwnd_array = win_tool.get_all_window_handles_by_name(window_name)
    if None is hwnd_array or 0 == len(hwnd_array):
        hwnd_array = [f"未找到{window_name}窗口"]
    hwnd_array_str = list(hwnd_array)

    # 创建下拉选择框
    combobox = ttk.Combobox(selection_frame, values=hwnd_array_str, width=20, state="readonly")
    combobox.current(0)  # 默认选择第一个元素
    combobox.pack(side=tk.LEFT, padx=10)

    btn_print_selection = tk.Button(selection_frame, text="激活窗口(后面的功能基于此窗口)", width=28, height=1,
                                    command=active_window)
    btn_print_selection.pack(side=tk.LEFT, padx=10)

    btn_auto_attack = tk.Button(selection_frame, text="自动攻击", width=14, height=1, command=auto_attack)
    btn_auto_attack.pack(side=tk.LEFT, padx=10)

    btn_auto_collect = tk.Button(selection_frame, text="自动拾取", width=14, height=1, command=auto_collect)
    btn_auto_collect.pack(side=tk.LEFT, padx=10)

    # 底部
    # bottom_frame = tk.Frame(scrollable_frame)
    # bottom_frame.pack(pady=20, side=tk.TOP, fill="x", anchor="w")
    #
    # # 底部一张图
    # image = Image.open(win_tool.resource_path("img/shibadafutou.png"))  # 使用 PIL 加载图片
    # image = image.resize((186, 334), Image.LANCZOS)
    # photo = ImageTk.PhotoImage(image)
    # img_label = tk.Label(bottom_frame, image=photo).pack(side=tk.LEFT, padx=10)
    #
    # image2 = Image.open(win_tool.resource_path("img/yangwanli.png"))
    # image2 = image2.resize((200, 334), Image.LANCZOS)
    # photo2 = ImageTk.PhotoImage(image2)
    # img_label2 = tk.Label(bottom_frame, image=photo2).pack(side=tk.LEFT, padx=10)
    #
    # image3 = Image.open(win_tool.resource_path("img/dashicunlaogou.png"))
    # image3 = image3.resize((186, 334), Image.LANCZOS)
    # photo3 = ImageTk.PhotoImage(image3)
    # img_label3 = tk.Label(bottom_frame, image=photo3).pack(side=tk.LEFT, padx=10)

    # 使用 keyboard 绑定全局快捷键
    keyboard.add_hotkey('F12', stop_all_script)

    # 启动激活窗口，子线程
    # t = threading.Thread(target=app.active_game_window, args=(hwnd_array[0], ), daemon=True)
    # t.start()

    root.bind("<Button-1>", root_click)
    # app.start_release_job()
    root.mainloop()
