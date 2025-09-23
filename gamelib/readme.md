

## 运行环境

打包的程序，需要安装微软运行库。

```
https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-160
https://aka.ms/vs/17/release/vc_redist.x64.exe
```


### 依赖

```
pip install keyboard
pip install pywin32
pip install psutil
pip install pywinauto
pip install pyautogui

```

### 安装正确的 OpenCV

``` 
pip uninstall opencv-python opencv-python-headless opencv-contrib-python -y

pip install opencv-python

```

### 打包

打包工具
```
pip install pyinstaller

```

打包命令
```

pyinstaller --onefile --windowed --uac-admin --add-data "img/*;img"  application.py






# 增加 paddleocr 资源
--add-data "path_to_paddleocr_dir;./paddleocr"

创建可执行文件时请求管理员权限
将 Python 脚本打包成 .exe 文件，并且希望每次执行时都请求管理员权限，可以在 PyInstaller 打包时添加管理员权限请求。
可以通过修改 .spec 文件或使用 --uac-admin 标志来请求管理员权限。

pyinstaller --uac-admin your_script.py

```


清理缓存打包
```
pyinstaller --onefile --windowed --clean --noconfirm your_script.py

```



