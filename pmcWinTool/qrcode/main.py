import tkinter as tk
from PIL import Image, ImageTk
import qrcode
import io

def make_qr(event=None):
    text = entry.get().strip()
    if not text:
        return
    qr_img = qrcode.make(text)
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    buf.seek(0)
    img = Image.open(buf).resize((200, 200))  # 固定二维码显示尺寸
    tk_img = ImageTk.PhotoImage(img)

    qr_label.config(image=tk_img)
    qr_label.image = tk_img  # 防止被回收

    # 更新二维码文字
    qr_text_label.config(text=text)

# 复制二维码文字到剪贴板
def copy_text(event=None):
    text = qr_text_label.cget("text")
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()

root = tk.Tk()
root.title("PMC 文字转二维码  blog.pandamancoin.com")
root.geometry("400x400")  # 固定窗口大小
root.resizable(False, False)

# 输入框
entry = tk.Entry(root, width=45)
entry.pack(pady=10)
entry.bind("<Return>", make_qr)  # 回车生成二维码

# 按钮
btn = tk.Button(root, text="生成二维码", command=make_qr)
btn.pack(pady=5)

# 提前放占位二维码图片
placeholder = Image.new("RGB", (200, 200), "white")
ph_img = ImageTk.PhotoImage(placeholder)
qr_label = tk.Label(root, image=ph_img, width=200, height=200)
qr_label.image = ph_img
qr_label.pack(pady=5)

# 显示二维码内容的文字标签（点击可复制）
qr_text_label = tk.Label(root, text="", wraplength=320, fg="blue", cursor="hand2", justify="center")
qr_text_label.pack(pady=5)
qr_text_label.bind("<Button-1>", copy_text)  # 点击复制

root.mainloop()
