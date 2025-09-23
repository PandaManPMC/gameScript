import ctypes
from ctypes import wintypes
import win32gui, win32ui

def capture_window_area(hwnd, x=0, y=0, w=None, h=None):
    import ctypes
    from ctypes import windll
    import win32gui, win32ui
    from PIL import Image

    # 获取窗口矩形
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    win_w, win_h = right - left, bottom - top

    if w is None: w = win_w
    if h is None: h = win_h

    if 0 != x and w > x:
        w = w - x
    if 0 != y and h > y:
        h = h - y

    # 创建设备上下文
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, win_w, win_h)
    saveDC.SelectObject(saveBitMap)

    # 调用 PrintWindow
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

    # 转换成 PIL.Image
    bmpinfo = saveBitMap.GetInfo()
    bmpstr  = saveBitMap.GetBitmapBits(True)
    img = Image.frombuffer(
        "RGB",
        (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
        bmpstr, "raw", "BGRX", 0, 1
    )

    # 裁剪子区域
    img = img.crop((x, y, x + w, y + h))

    # 清理
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return img if result == 1 else None
