import cv2
import numpy as np
import win32gui
import win32ui
import win32con
from PIL import Image
import win_tool

# 截取窗口图像
def capture_window(hwnd, x_offset=0, y_offset=0, capture_width=None, capture_height=None):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    # 如果没有提供宽高，默认截取整个窗口
    if capture_width is None:
        capture_width = w
    if capture_height is None:
        capture_height = h

    # 限定截图范围，确保不超出窗口边界
    # capture_width = min(capture_width, w - x_offset)
    # capture_height = min(capture_height, h - y_offset)
    print(f"x_offset = {x_offset} y_offset={y_offset} capture_width={capture_width}, capture_height={capture_height}")
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, capture_width, capture_height)
    saveDC.SelectObject(saveBitMap)

    # 仅截取指定范围的区域
    saveDC.BitBlt((0, 0), (capture_width, capture_height), mfcDC, (x_offset, y_offset), win32con.SRCCOPY)
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
                print(f"找到匹配项={template_img_path}，位置: {pt}，大小: ({int(w * scale)}, {int(h * scale)})")
                return pt  # 返回匹配的坐标

    print(f"未找到匹配项={template_img_path}")

    # 显示结果
    # cv2.imshow("Result", np.array(screen_img))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return None


# 工具函数：查找图像并返回坐标（坐标需要加上偏移的 x,y）
def find_image_in_window(hwnd, template_img_path, x_offset=0, y_offset=0, capture_width=None,
                         capture_height=None, threshold=0.7):
    if hwnd is None:
        return None

    # 截取游戏窗口的图像（限制范围）
    screen_img = capture_window(hwnd, x_offset, y_offset, capture_width, capture_height)

    # 使用多尺度模板匹配，并获取匹配的坐标
    match_location = multi_scale_template_matching(screen_img, template_img_path, threshold)

    if match_location:
        return match_location  # 返回匹配坐标 (x, y)
    return None


# 示例用法
if __name__ == "__main__":
    window_name = "夏禹剑 - 刀剑2"  # 替换为你的游戏窗口名称
    template_img_path = "./img/dahuang.bmp"  # 替换为你要匹配的模板图片路径

    hwnd = win_tool.get_window_handle(window_name)
    w, h = win_tool.get_win_w_h()

    # 设置截图范围，x_offset, y_offset, capture_width, capture_height
    match_location = find_image_in_window(hwnd, template_img_path, 400, 300, int(w * 0.5), int(h * 0.5))
    if match_location:
        print(f"图像匹配成功，坐标: {match_location}")
    else:
        print("图像匹配失败")
