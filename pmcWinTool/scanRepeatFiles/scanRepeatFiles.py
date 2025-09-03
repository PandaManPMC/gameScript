import os
import hashlib
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from collections import defaultdict
import threading

def get_file_hash(file_path, hash_algo='md5', chunk_size=8192):
    """计算文件的哈希值"""
    hash_func = hashlib.new(hash_algo)
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def find_duplicate_files(directory):
    """扫描目录，找到重复文件"""
    duplicates = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_hash = get_file_hash(file_path)
                duplicates[file_hash].append(file_path)
            except Exception as e:
                print(f"无法处理文件 {file_path}: {e}")

    return {h: paths for h, paths in duplicates.items() if len(paths) > 1}

def select_directory():
    folder = filedialog.askdirectory()
    if folder:
        entry_dir.delete(0, tk.END)
        entry_dir.insert(0, folder)

def scan_worker(folder):
    """子线程执行扫描"""
    duplicates = find_duplicate_files(folder)

    # 扫描完成后更新 UI（回到主线程）
    def update_ui():
        text_output.delete(1.0, tk.END)
        if not duplicates:
            text_output.insert(tk.END, "未发现重复文件。")
        else:
            text_output.insert(tk.END, "发现重复文件：\n")
            for hash_val, files in duplicates.items():
                text_output.insert(tk.END, f"\n哈希值: {hash_val}\n")
                for file in files:
                    text_output.insert(tk.END, f"  {file}\n")

        # 恢复按钮
        btn_scan.config(text="扫描", state="normal")

    root.after(0, update_ui)

def scan_directory():
    folder = entry_dir.get()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("错误", "请选择一个有效的目录！")
        return

    # 清空输出
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, "正在扫描，请稍候...\n")

    # 按钮改为“扫描中”，并禁用
    btn_scan.config(text="扫描中...", state="disabled")

    # 启动子线程
    threading.Thread(target=scan_worker, args=(folder,), daemon=True).start()

# 创建主窗口
root = tk.Tk()
root.title("重复文件扫描器")
root.geometry("700x500")

# 目录选择部分
frame_dir = tk.Frame(root)
frame_dir.pack(pady=10, padx=10, fill="x")

entry_dir = tk.Entry(frame_dir)
entry_dir.pack(side="left", fill="x", expand=True, padx=5)

btn_browse = tk.Button(frame_dir, text="选择目录", command=select_directory)
btn_browse.pack(side="left", padx=5)

btn_scan = tk.Button(frame_dir, text="扫描", command=scan_directory)
btn_scan.pack(side="left", padx=5)

# 输出文本框（带滚动条）
text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=25)
text_output.pack(padx=10, pady=10, fill="both", expand=True)

# 运行主循环
root.mainloop()
