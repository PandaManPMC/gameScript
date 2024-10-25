import cv2
import numpy as np
import win32gui
import win32ui
import win32con
import win32api
from PIL import Image

# 截取窗口图像
def capture_window(hwnd):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )

    return img

# 使用多尺度模板匹配查找目标图像，并返回匹配位置的坐标
def multi_scale_template_matching(screen_img, template_img_path, threshold=0.8):
    screen_gray = cv2.cvtColor(np.array(screen_img), cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_img_path, 0)  # 读取模板图片（灰度）

    h, w = template.shape

    # 定义尺度范围，模板从 50% 到 150% 大小变化
    for scale in np.linspace(0.5, 1.5, 20)[::-1]:
        resized_template = cv2.resize(template, (int(w * scale), int(h * scale)))
        res = cv2.matchTemplate(screen_gray, resized_template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        # 找到匹配
        if len(loc[0]) > 0:
            for pt in zip(*loc[::-1]):
                print(f"找到匹配项，位置: {pt}，大小: ({int(w * scale)}, {int(h * scale)})")
                return pt  # 返回匹配的坐标

    print("未找到匹配项")
    return None

# 工具函数：查找图像并返回坐标
def find_image_in_window(hwnd, template_img_path, threshold=0.8):
    if hwnd is None:
        return None

    # 截取游戏窗口的图像
    screen_img = capture_window(hwnd)

    # 使用多尺度模板匹配，并获取匹配的坐标
    match_location = multi_scale_template_matching(screen_img, template_img_path, threshold)

    if match_location:
        return match_location  # 返回匹配坐标 (x, y)
    return None


# 示例用法
if __name__ == "__main__":
    window_name = "夏禹剑 - 刀剑2"  # 替换为你的游戏窗口名称
    template_img_path = "./img/jiufeng_jiaogeiwoba.bmp"  # 替换为你要匹配的模板图片路径

    match_location = find_image_in_window(window_name, template_img_path)
    if match_location:
        print(f"图像匹配成功，坐标: {match_location}")
    else:
        print("图像匹配失败")
