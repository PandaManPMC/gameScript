### 打包

打包工具
```
pip install pyinstaller

```

打包命令
```
pyinstaller --onefile --windowed main.py

pyinstaller --onefile --windowed --uac-admin --add-data "img/*;img"  main.py

```
