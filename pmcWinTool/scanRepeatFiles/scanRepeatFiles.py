import os
import hashlib
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from collections import defaultdict
import threading

stop_flag = False   # 全局停止标志
duplicate_results = {}  # 保存扫描结果

def get_file_hash(file_path, hash_algo='md5', chunk_size=8192):
    """计算文件的哈希值"""
    hash_func = hashlib.new(hash_algo)
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def list_all_files(directory):
    """获取目录下所有文件路径"""
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def find_duplicate_files(file_list, progress_callback):
    """扫描文件列表，找到重复文件"""
    duplicates = defaultdict(list)
    total = len(file_list)

    for idx, file_path in enumerate(file_list, start=1):
        if stop_flag:  # 检查是否需要停止
            break
        try:
            file_hash = get_file_hash(file_path)
            duplicates[file_hash].append(file_path)
        except Exception as e:
            print(f"无法处理文件 {file_path}: {e}")

        progress_callback(idx, total)  # 更新进度

    return {h: paths for h, paths in duplicates.items() if len(paths) > 1}

def select_directory():
    folder = filedialog.askdirectory()
    if folder:
        entry_dir.delete(0, tk.END)
        entry_dir.insert(0, folder)

def scan_worker(folder):
    global stop_flag, duplicate_results
    stop_flag = False

    file_list = list_all_files(folder)

    def progress_callback(current, total):
        percent = int(current / total * 100)
        root.after(0, lambda: progress_bar.config(value=percent))
        root.after(0, lambda: lbl_progress.config(text=f"进度: {percent}%"))

    duplicates = find_duplicate_files(file_list, progress_callback)
    duplicate_results = duplicates  # 保存扫描结果

    # 扫描完成后更新 UI
    def update_ui():
        text_output.delete(1.0, tk.END)
        if stop_flag:
            text_output.insert(tk.END, "扫描已停止。")
            btn_delete.config(state="disabled")
        elif not duplicates:
            text_output.insert(tk.END, "未发现重复文件。")
            btn_delete.config(state="disabled")
        else:
            text_output.insert(tk.END, "发现重复文件：\n")
            for hash_val, files in duplicates.items():
                text_output.insert(tk.END, f"\n哈希值: {hash_val}\n")
                for file in files:
                    text_output.insert(tk.END, f"  {file}\n")
            btn_delete.config(state="normal")  # 启用删除按钮

        # 恢复按钮状态
        btn_scan.config(text="扫描", state="normal")
        btn_stop.config(state="disabled")
        progress_bar["value"] = 0
        lbl_progress.config(text="进度: 0%")

    root.after(0, update_ui)

def scan_directory():
    folder = entry_dir.get()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("错误", "请选择一个有效的目录！")
        return

    # 清空输出
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, "正在扫描，请稍候...\n")

    # 修改按钮状态
    btn_scan.config(text="扫描中...", state="disabled")
    btn_stop.config(state="normal")
    btn_delete.config(state="disabled")

    # 启动子线程
    threading.Thread(target=scan_worker, args=(folder,), daemon=True).start()

def stop_scan():
    global stop_flag
    stop_flag = True

def delete_duplicates():
    global duplicate_results
    if not duplicate_results:
        messagebox.showinfo("提示", "没有可删除的重复文件。")
        return

    confirm = messagebox.askyesno("确认", "确定要删除重复文件吗？（每组只保留第一个）")
    if not confirm:
        return

    # 禁用删除按钮
    btn_delete.config(state="disabled")

    deleted_files = []
    for hash_val, files in duplicate_results.items():
        # 保留第一个文件，删除后续
        for file in files[1:]:
            try:
                os.remove(file)
                deleted_files.append(file)
            except Exception as e:
                print(f"删除失败 {file}: {e}")

    # 更新输出框
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, "\n\n已删除以下重复文件：\n")
    for file in deleted_files:
        text_output.insert(tk.END, f"  {file}\n")

    messagebox.showinfo("完成", f"已删除 {len(deleted_files)} 个重复文件。")


# 创建主窗口
root = tk.Tk()
root.title("PMC 重复文件管理 blog.pandamancoin.com")
root.geometry("750x600")

# 目录选择部分
frame_dir = tk.Frame(root)
frame_dir.pack(pady=10, padx=10, fill="x")

entry_dir = tk.Entry(frame_dir)
entry_dir.pack(side="left", fill="x", expand=True, padx=5)

btn_browse = tk.Button(frame_dir, text="选择目录", command=select_directory)
btn_browse.pack(side="left", padx=5)

btn_scan = tk.Button(frame_dir, text="扫描", command=scan_directory)
btn_scan.pack(side="left", padx=5)

btn_stop = tk.Button(frame_dir, text="停止", command=stop_scan, state="disabled")
btn_stop.pack(side="left", padx=5)

btn_delete = tk.Button(frame_dir, text="删除重复", command=delete_duplicates, state="disabled")
btn_delete.pack(side="left", padx=5)

# 进度条
frame_progress = tk.Frame(root)
frame_progress.pack(pady=5, padx=10, fill="x")

progress_bar = ttk.Progressbar(frame_progress, orient="horizontal", mode="determinate")
progress_bar.pack(side="left", fill="x", expand=True, padx=5)

lbl_progress = tk.Label(frame_progress, text="进度: 0%")
lbl_progress.pack(side="left")

# 输出文本框（带滚动条）
text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=25)
text_output.pack(padx=10, pady=10, fill="both", expand=True)

# 运行主循环
root.mainloop()
