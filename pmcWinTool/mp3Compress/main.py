

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")


def compress_mp3_folder(input_folder, output_folder, bitrate="64k"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    count = 0
    for file in os.listdir(input_folder):
        if file.lower().endswith(".mp3"):
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, file)

            audio = AudioSegment.from_mp3(input_path)
            audio.export(output_path, format="mp3", bitrate=bitrate)
            count += 1

    return count

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        input_folder.set(folder)

def start_compression():
    folder = input_folder.get()
    if not folder:
        messagebox.showwarning("提示", "请先选择一个文件夹！")
        return

    output_folder = os.path.join(folder, "output")
    try:
        count = compress_mp3_folder(folder, output_folder, bitrate=bitrate.get())
        messagebox.showinfo("完成", f"共压缩 {count} 个 MP3 文件\n输出目录：{output_folder}")
    except Exception as e:
        messagebox.showerror("错误", f"压缩失败：{e}")


# 窗口 UI
root = tk.Tk()
root.title("PMC MP3 批量压缩工具 blog.pandamancoin.com")
root.geometry("400x400")

input_folder = tk.StringVar()
bitrate = tk.StringVar(value="128k")

tk.Label(root, text="选择文件夹:").pack(pady=5)
tk.Entry(root, textvariable=input_folder, width=40).pack(pady=5)
tk.Button(root, text="浏览", command=select_folder).pack(pady=5)

tk.Label(root, text="比特率 (例如 128k, 64k, 32k):").pack(pady=5)
tk.Entry(root, textvariable=bitrate).pack(pady=5)

tk.Button(root, text="开始压缩", command=start_compression).pack(pady=20)

root.mainloop()
