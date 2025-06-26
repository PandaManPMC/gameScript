import tkinter as tk

class CustomWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x480")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.99)

        self.is_topmost = True

        # 自定义标题栏
        self.title_bar = tk.Frame(self.root, bg="#cceeff", relief="raised", bd=0)
        self.title_bar.pack(fill=tk.X)

        self.title_label = tk.Label(self.title_bar, text="PMC 便签", bg="#cceeff", fg="black")
        self.title_label.pack(side=tk.LEFT, padx=10)

        self.pin_button = tk.Button(self.title_bar, text="📍", bg="#cceeff", fg="black",
                                    command=self.toggle_topmost, relief="flat", borderwidth=0)
        self.pin_button.pack(side=tk.RIGHT, padx=5)

        self.close_button = tk.Button(self.title_bar, text="✖", bg="#cceeff", fg="black",
                                      command=self.root.destroy, relief="flat", borderwidth=0)
        self.close_button.pack(side=tk.RIGHT, padx=5)

        # 主体文本区域容器，设置padding
        self.text_frame = tk.Frame(self.root, padx=8, pady=8)
        self.text_frame.pack(expand=True, fill="both")

        # 文本输入框，自动换行，字体美观
        self.text_area = tk.Text(self.text_frame, bg="white", fg="black",
                                 font=("Arial", 11), wrap="word", undo=True)
        self.text_area.pack(expand=True, fill="both")

        # 缩放区域
        self.resizer = tk.Frame(self.root, cursor="bottom_right_corner", bg="#cceeff", width=10, height=10)
        self.resizer.place(relx=1.0, rely=1.0, anchor="se")

        # 拖动窗口
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        # 缩放绑定
        self.resizer.bind("<ButtonPress-1>", self.start_resize)
        self.resizer.bind("<B1-Motion>", self.do_resize)

    def toggle_topmost(self):
        self.is_topmost = not self.is_topmost
        self.root.attributes("-topmost", self.is_topmost)
        self.pin_button.config(text="📌" if not self.is_topmost else "📍")

    def start_move(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def do_move(self, event):
        x = event.x_root - self._drag_x
        y = event.y_root - self._drag_y
        self.root.geometry(f'+{x}+{y}')

    def start_resize(self, event):
        self._resize_start_x = event.x
        self._resize_start_y = event.y
        self._start_width = self.root.winfo_width()
        self._start_height = self.root.winfo_height()

    def do_resize(self, event):
        dx = event.x - self._resize_start_x
        dy = event.y - self._resize_start_y
        new_width = max(300, self._start_width + dx)
        new_height = max(200, self._start_height + dy)
        self.root.geometry(f"{new_width}x{new_height}")
        self.resizer.place(relx=1.0, rely=1.0, anchor="se")


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomWindow(root)
    root.mainloop()
