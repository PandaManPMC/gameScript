


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


pyinstaller --onefile --windowed --uac-admin --add-data "img/*;img" --add-data "D:\a\codes\game_script\pythonProject\.venv\Lib\site-packages\paddleocr;./paddleocr" --add-data "D:\a\codes\game_script\pythonProject\.venv\Lib\site-packages\paddle;./paddle" --hidden-import shapely.geometry --hidden-import numpy --hidden-import cv2 --hidden-import PIL --hidden-import yaml --hidden-import requests --hidden-import tqdm --hidden-import scipy --hidden-import pyclipper --hidden-import skimage --hidden-import flask --hidden-import chardet --hidden-import nltk --hidden-import skimage --hidden-import skimage.morphology --hidden-import skimage.morphology._skeletonize --hidden-import imgaug --hidden-import albumentations --hidden-import docx --hidden-import lxml dao2_control.py


 
--hidden-import albumentations
--hidden-import docx \
--hidden-import lxml \

--hidden-import shapely.geometry \
--hidden-import numpy \
--hidden-import cv2 \
--hidden-import PIL \
--hidden-import yaml \
--hidden-import requests \
--hidden-import tqdm \
--hidden-import scipy \
--hidden-import pyclipper \
--hidden-import skimage \
--hidden-import flask \
--hidden-import chardet \
--hidden-import nltk \
--hidden-import skimage \
--hidden-import skimage.morphology \
--hidden-import skimage.morphology._skeletonize \
--hidden-import imgaug \



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


## 图像对比

### 依赖

图片转文字 pytesseract


```
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install pytesseract -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install pyautogui
pip install keyboard

```

图文识别的另一个，无需 pytesseract，是独立的
```
pip install easyocr -i https://pypi.tuna.tsinghua.edu.cn/simple/

百度的 paddleocr 中文识别
pip install paddleocr -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install paddlepaddle  -i https://pypi.tuna.tsinghua.edu.cn/simple/

```

EasyOCR：
专注于图片中的文本提取（OCR）。
提供开箱即用的 OCR 功能，简单易用。

Torch：
是一个通用的深度学习框架。
提供 EasyOCR 所需的底层支持（如张量计算和 GPU 加速）。

### 环境

需要安装 Tesseract OCR 软件，你可以从以下地址下载安装：

Tesseract OCR
安装完成后，将 Tesseract 的路径添加到系统环境变量，或者在 Python 中手动指定路径。

```
https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe
```
