

```angular2html
pip install --upgrade "pillow[avif]"
pip install --upgrade "pillow[webp]"

pip install pillow[avif]
pip install pillow[webp]
```


### 打包

打包工具
```
pip install pyinstaller
```

打包命令
```
pyinstaller --onefile --windowed main.py

pyinstaller --onefile --windowed --name imageConversion main.py

pyinstaller --onefile --windowed --uac-admin --add-data "img/*;img"  main.py

```


