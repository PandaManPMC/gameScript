import os
from tkinter import filedialog, Tk, Label, Button, IntVar, Checkbutton, Entry
from PIL import Image

root = Tk()
root.title("PMC 图片批量转换器 blog.pandamancoin.com")
root.geometry("480x380")
root.resizable(False, False)

quality_var = IntVar(value=100)
lossless_var = IntVar(value=0)

Label(root, text="PNG/JPG/WEBP ➜ AVIF/WebP 批量转换器", font=("Arial", 14)).pack(pady=10)
Label(root, text="输出质量 (1-100)：").pack()
quality_entry = Entry(root, textvariable=quality_var, width=5)
quality_entry.pack()
Checkbutton(root, text="无损压缩（忽略上方设置）", variable=lossless_var).pack(pady=5)

def convert_images():
    folder_selected = filedialog.askdirectory(title="选择图片文件夹")
    if not folder_selected:
        return

    avif_folder = os.path.join(folder_selected, "avif_output")
    webp_folder = os.path.join(folder_selected, "webp_output")
    os.makedirs(avif_folder, exist_ok=True)
    os.makedirs(webp_folder, exist_ok=True)

    count = 0
    for filename in os.listdir(folder_selected):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            input_path = os.path.join(folder_selected, filename)
            avif_path = os.path.join(avif_folder, os.path.splitext(filename)[0] + ".avif")
            webp_path = os.path.join(webp_folder, os.path.splitext(filename)[0] + ".webp")
            try:
                img = Image.open(input_path)
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")

                # 转 AVIF
                if lossless_var.get():
                    img.save(avif_path, format="AVIF", lossless=True)
                else:
                    quality_val = max(1, min(quality_var.get(), 100))
                    img.save(avif_path, format="AVIF", quality=quality_val)

                # 转 WebP
                if lossless_var.get():
                    img.save(webp_path, format="WEBP", lossless=True)
                else:
                    quality_val = max(1, min(quality_var.get(), 100))
                    img.save(webp_path, format="WEBP", quality=quality_val)

                count += 1
            except Exception as e:
                print(f"转换失败: {filename}, 原因: {e}")

    Label(root, text=f"转换完成，共 {count} 张图像。", fg="green").pack()

Button(root, text="选择文件夹并开始转换", command=convert_images).pack(pady=15)

root.mainloop()
