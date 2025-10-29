
# winBox 工具箱

```
pyinstaller --onefile --windowed --uac-admin --add-data "img/*;img" --paths "../../" winBox.py

pyinstaller --onefile --windowed --uac-admin --add-data "img/*;img" --paths "../../" --hidden-import pyautogui --hidden-import mouseinfo --hidden-import win32gui --hidden-import win32api --hidden-import win32con --hidden-import win32ui --hidden-import pyscreeze --hidden-import PIL.Image --hidden-import PIL.ExifTags --hidden-import PIL._tkinter_finder winBox.py


```


