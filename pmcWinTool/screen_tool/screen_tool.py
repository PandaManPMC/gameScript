import tkinter as tk
import pyautogui
import threading
import keyboard
import mouse
import time

class MouseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PMC 鼠标位置监测工具(F12停止)")
        self.root.geometry("520x240")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)  # 窗口置顶

        self.running = False

        # 界面组件
        self.label_info = tk.Label(root, text="点击开始按钮以检测鼠标位置(F12停止)", font=("微软雅黑", 10))
        self.label_info.pack(pady=20)

        self.label_data = tk.Label(root, text="", font=("Consolas", 12), fg="blue")
        self.label_data.pack(pady=10)

        self.btn_start = tk.Button(root, text="开始检测(F12停止)", width=15, height=2, command=self.toggle_tracking)
        self.btn_start.pack(pady=10)

        self.screen_width, self.screen_height = pyautogui.size()

        # 绑定 F12 停止
        keyboard.add_hotkey("F12", self.stop_tracking)

    def toggle_tracking(self):
        if not self.running:
            self.running = True
            self.btn_start.config(text="检测中...", state="disabled")
            self.label_info.config(text="移动鼠标查看坐标\n点击鼠标左键或按 F12 停止")
            threading.Thread(target=self.track_mouse, daemon=True).start()
        else:
            self.stop_tracking()

    def track_mouse(self):
        mouse.hook(self.mouse_click_stop)

        while self.running:
            x, y = pyautogui.position()
            px = (x / self.screen_width) * 100
            py = (y / self.screen_height) * 100

            text = f"X = {x:<5} ({px:6.2f}%)\nY = {y:<5} ({py:6.2f}%)"
            self.label_data.config(text=text)
            time.sleep(0.05)

        mouse.unhook(self.mouse_click_stop)
        self.btn_start.config(text="开始检测", state="normal")
        self.label_info.config(text="检测已停止（坐标保留）")
        # ✅ 不再清空 self.label_data，让最后的坐标保留显示
        # self.label_data.config(text="")  ← 已删除

    def mouse_click_stop(self, event):
        # 只在 MouseEvent 有 event_type 属性时才判断
        if hasattr(event, "event_type") and event.event_type == "down" and getattr(event, "button", None) == "left":
            self.stop_tracking()

    def stop_tracking(self):
        self.running = False

def main():
    root = tk.Tk()
    app = MouseTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
