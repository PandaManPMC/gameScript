import os
import sys
import traceback
from ctypes import windll
import win32gui, win32ui
from PIL import Image
import cv2
import numpy as np


def resource_path(relative_path):
    """获取资源文件的绝对路径，打包后也能正确访问"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后存放临时文件的路径
        base_path = sys._MEIPASS
    else:
        # 开发环境中的路径
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def capture_window_area(hwnd, x=0, y=0, w=None, h=None):
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


def find_image_in_window(hwnd, template_path,x=0, y=0, w=None, h=None, threshold=0.8, debug=False):
    """在指定窗口截图中查找模板图片，返回匹配位置"""
    screenshot = capture_window_area(hwnd,x,y,w,h)
    if screenshot is None:
        print(f"❌{template_path} PrintWindow 截图失败")
        return None

    # 转为 OpenCV 格式
    screen_np = np.array(screenshot)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)
    template = cv2.imread(resource_path(template_path), cv2.IMREAD_GRAYSCALE)

    if template is None:
        raise FileNotFoundError(f"模板图片未找到: {template_path}")

    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        t_h, t_w = template.shape[:2]
        center_x = max_loc[0] + t_w // 2
        center_y = max_loc[1] + t_h // 2
        print(f"✅ {template_path} 匹配成功: ({center_x}, {center_y}) 相似度 {max_val:.3f}")

        if debug:
            cv2.rectangle(screen_np, max_loc, (max_loc[0] + t_w, max_loc[1] + t_h), (0, 255, 0), 2)
            cv2.imshow("Match", cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return (center_x + x, center_y + y, max_val)
    else:
        print(f"❌{template_path} 未找到匹配（最大相似度 {max_val:.3f}）")
        return None