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


def find_image_in_window_v1(hwnd, template_path,x=0, y=0, w=None, h=None, threshold=0.8, debug=False):
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




def capture_window_area_v2(hwnd, x=0, y=0, w=None, h=None):
    """后台截图（使用 PrintWindow），返回 PIL.Image"""
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    win_w, win_h = right - left, bottom - top

    if w is None: w = win_w
    if h is None: h = win_h

    if 0 != x and w > x:
        w = w - x
    if 0 != y and h > y:
        h = h - y

    # 创建兼容 DC
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, win_w, win_h)
    saveDC.SelectObject(saveBitMap)

    # PrintWindow 获取窗口内容
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

    # 转为 Image
    bmpinfo = saveBitMap.GetInfo()
    bmpstr  = saveBitMap.GetBitmapBits(True)
    img = Image.frombuffer(
        "RGB",
        (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
        bmpstr, "raw", "BGRX", 0, 1
    )

    # 裁剪区域
    img = img.crop((x, y, x + w, y + h))

    # 清理
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result != 1:
        return None
    return img


def find_image_in_window(hwnd, template_path, x=0, y=0, w=None, h=None,
                         threshold=0.85, debug=False, use_edge=False):
    """在窗口截图中查找模板图片（自动灰度、模糊、DPI 缩放）"""
    screenshot = capture_window_area_v2(hwnd, x, y, w, h)
    if screenshot is None:
        print(f"❌ PrintWindow 截图失败: {template_path}")
        return None

    # 转灰度图 + 模糊
    screen_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    template = cv2.imread(resource_path(template_path), cv2.IMREAD_GRAYSCALE)

    if template is None:
        print(f"❌ 模板图片未找到: {template_path}")
        return None

    # 模糊降噪，抵消色差和压缩噪点
    screen_gray = cv2.GaussianBlur(screen_gray, (3, 3), 0)
    template = cv2.GaussianBlur(template, (3, 3), 0)

    # 如果想对比形状，不依赖颜色，可开启边缘模式
    if use_edge:
        screen_gray = cv2.Canny(screen_gray, 50, 150)
        template = cv2.Canny(template, 50, 150)

    best_val, best_loc, best_scale = 0, None, 1.0

    # 自动多尺度匹配，解决 DPI / 缩放比例问题
    for scale in np.linspace(0.9, 1.1, 9):  # 支持 ±10% 尺寸变化
        resized = cv2.resize(template, None, fx=scale, fy=scale)
        res = cv2.matchTemplate(screen_gray, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > best_val:
            best_val, best_loc, best_scale = max_val, max_loc, scale

    if best_val >= threshold:
        h_t, w_t = template.shape[:2]
        cx = best_loc[0] + int(w_t * best_scale / 2)
        cy = best_loc[1] + int(h_t * best_scale / 2)
        print(f"✅ 匹配成功 {template_path}: ({cx},{cy}) 相似度 {best_val:.3f}")

        if debug:
            screen_vis = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            cv2.rectangle(screen_vis, best_loc,
                          (best_loc[0] + int(w_t * best_scale),
                           best_loc[1] + int(h_t * best_scale)),
                          (0, 255, 0), 2)
            cv2.imshow("Match Debug", screen_vis)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return (cx + x, cy + y, best_val)
    else:
        print(f"❌ 未匹配 {template_path}，最大相似度 {best_val:.3f}")
        return None