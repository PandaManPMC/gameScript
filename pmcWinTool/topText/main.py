import os
import sys
import tkinter as tk
import time

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


SAVE_FILE = os.path.join(os.path.expanduser("~"), ".pmc_note_temp.txt")


class CustomWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x480")
        self.root.title("PMC 便签 blog.pandamancoin.com")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.99)
        self.root.iconbitmap(resource_path("img/pmc.ico"))
        self.is_topmost = True
        self.last_saved_text = ""

        # 工具栏
        self.toolbar = tk.Frame(self.root, bg="#ddeeff", height=30)
        self.toolbar.pack(fill=tk.X, side=tk.TOP)

        # 添加保存按钮
        self.save_button = tk.Button(self.toolbar, text="💾 保存", bg="#ddeeff", fg="black",
                                     command=self.manual_save, relief="flat", borderwidth=0)
        self.save_button.pack(side=tk.RIGHT, padx=5, pady=2)

        # 添加置顶按钮
        self.pin_button = tk.Button(self.toolbar, text="📍 置顶", bg="#ddeeff", fg="black",
                                    command=self.toggle_topmost, relief="flat", borderwidth=0)
        self.pin_button.pack(side=tk.RIGHT, padx=5, pady=2)

        # 文本区域
        self.text_frame = tk.Frame(self.root, padx=8, pady=8)
        self.text_frame.pack(expand=True, fill="both")

        self.text_area = tk.Text(self.text_frame, bg="white", fg="black",
                                 font=("Arial", 11), wrap="word", undo=True)
        self.text_area.pack(expand=True, fill="both")

        self.load_temp_content()
        self.auto_save_loop()

    def toggle_topmost(self):
        self.is_topmost = not self.is_topmost
        self.root.attributes("-topmost", self.is_topmost)
        self.pin_button.config(text="📌置顶" if not self.is_topmost else "📍置顶")

    def load_temp_content(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.text_area.insert("1.0", content)
                    self.last_saved_text = content
            except Exception as e:
                print("加载临时内容失败:", e)

    def save_temp_content(self):
        current_text = self.text_area.get("1.0", "end-1c")
        if current_text != self.last_saved_text:
            try:
                with open(SAVE_FILE, "w", encoding="utf-8") as f:
                    f.write(current_text)
                self.last_saved_text = current_text
                print(f"[{time.strftime('%H:%M:%S')}] 自动保存完成")
            except Exception as e:
                print("自动保存失败:", e)

    def manual_save(self):
        current_text = self.text_area.get("1.0", "end-1c")
        if current_text != self.last_saved_text:
            try:
                with open(SAVE_FILE, "w", encoding="utf-8") as f:
                    f.write(current_text)
                self.last_saved_text = current_text
                print(f"[{time.strftime('%H:%M:%S')}] 手动保存完成")
            except Exception as e:
                print("手动保存失败:", e)
        else:
            print("内容未更改，无需保存。")

    def auto_save_loop(self):
        self.save_temp_content()
        self.root.after(10000, self.auto_save_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomWindow(root)
    root.mainloop()
