import tkinter as tk

class CustomWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x300")
        self.root.overrideredirect(True)  # 移除系统标题栏
        self.root.attributes("-topmost", False)
        self.root.attributes("-alpha", 0.96)  # 设置窗口整体轻微透明

        self.is_topmost = False

        # 自定义标题栏（淡蓝色 + 模拟半透明效果）
        self.title_bar = tk.Frame(self.root, bg="#cceeff", relief="raised", bd=0)  # 淡蓝色
        self.title_bar.pack(fill=tk.X)

        # 标题文本
        self.title_label = tk.Label(self.title_bar, text="PMC 便签", bg="#cceeff", fg="black")
        self.title_label.pack(side=tk.LEFT, padx=10)

        # 置顶按钮
        self.pin_button = tk.Button(self.title_bar, text="📌", bg="#cceeff", fg="black",
                                    command=self.toggle_topmost, relief="flat", borderwidth=0)
        self.pin_button.pack(side=tk.RIGHT, padx=5)

        # 关闭按钮
        self.close_button = tk.Button(self.title_bar, text="✖", bg="#cceeff", fg="black",
                                      command=self.root.destroy, relief="flat", borderwidth=0)
        self.close_button.pack(side=tk.RIGHT, padx=5)

        # 主体区域
        self.text_area = tk.Text(self.root, bg="white", fg="black", font=("Arial", 11))
        self.text_area.pack(expand=True, fill="both")

        # 启用拖动
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

    def toggle_topmost(self):
        self.is_topmost = not self.is_topmost
        self.root.attributes("-topmost", self.is_topmost)
        self.pin_button.config(text="📌" if not self.is_topmost else "📍")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f'+{x}+{y}')


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomWindow(root)
    root.mainloop()
