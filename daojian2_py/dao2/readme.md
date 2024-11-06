


## 运行环境

打包的程序，需要安装微软运行库。

```
https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-160
https://aka.ms/vs/17/release/vc_redist.x64.exe
```


## 群控

### 依赖

```
pip install pywin32
pip install psutil
pip install pywinauto

```


### 打包

打包工具
```
pip install pyinstaller

```

打包命令
```
pyinstaller --onefile --windowed your_script.py

pyinstaller --onefile --windowed --uac-admin --add-data "img/*;img"  dao2_control.py


创建可执行文件时请求管理员权限
将 Python 脚本打包成 .exe 文件，并且希望每次执行时都请求管理员权限，可以在 PyInstaller 打包时添加管理员权限请求。
可以通过修改 .spec 文件或使用 --uac-admin 标志来请求管理员权限。

pyinstaller --uac-admin your_script.py

```

清理缓存打包
```
pyinstaller --onefile --windowed --clean --noconfirm your_script.py

```


## 图像对比

### 依赖

```
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install pytesseract -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install pyautogui
pip install keyboard

```

### 环境

需要安装 Tesseract OCR 软件，你可以从以下地址下载安装：

Tesseract OCR
安装完成后，将 Tesseract 的路径添加到系统环境变量，或者在 Python 中手动指定路径。

```
https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe
```
