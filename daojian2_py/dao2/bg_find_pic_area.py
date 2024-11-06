from ctypes import wintypes

import cv2
import numpy as np
import win32gui
import win32ui
import win32con
from PIL import Image
import win_tool
import win32api
import traceback
import log3
import ctypes





def get_gdi_count():
    # 加载 user32.dll 库
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    # 定义 GetGuiResources 函数的返回类型和参数类型
    user32.GetGuiResources.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    user32.GetGuiResources.restype = wintypes.DWORD

    # 获取当前进程句柄
    hProcess = ctypes.windll.kernel32.GetCurrentProcess()

    # 0 表示 GDI 对象，1 表示 USER 对象
    gdi_count = user32.GetGuiResources(hProcess, 0)
    return gdi_count


def capture_window(hwnd, x_offset=0, y_offset=0, capture_width=None, capture_height=None, is_desktop_handle=False):
    hwndDC, mfcDC, saveDC, saveBitMap = None, None, None, None  # 初始化所有对象为 None
    try:
        # 检查 GDI 资源是否充足
        gdi_count = get_gdi_count()
        log3.logger.debug(f"GDI resources use {gdi_count}")
        # if gdi_count > 9000:  # 接近上限，暂停或终止截图
        #     log3.logger.error(f"GDI resources running low, skipping capture {gdi_count}")
        #     raise RuntimeError(f"GDI resources running low, skipping capture {gdi_count}") # from e

        # 获取窗口位置和大小
        scale = win_tool.get_screen_scale()

        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top

        if not is_desktop_handle:
            w = win_tool.calculate_physical_pixels(w, scale)
            h = win_tool.calculate_physical_pixels(h, scale)

        # 默认使用整个窗口大小
        if capture_width is None:
            capture_width = w
        else:
            if not is_desktop_handle:
                capture_width = win_tool.calculate_physical_pixels(capture_width, scale) - x_offset
            else:
                capture_width -= x_offset
        if capture_height is None:
            capture_height = h
        else:
            if not is_desktop_handle:
                capture_height = win_tool.calculate_physical_pixels(capture_height, scale) - y_offset
            else:
                capture_height -= y_offset

        # 限制截图范围，确保不超出边界
        # capture_width = min(capture_width, w - x_offset)
        # capture_height = min(capture_height, h - y_offset)

        print(
            f"hwnd = {hwnd} scale = {scale} x_offset = {x_offset} y_offset={y_offset} capture_width={capture_width}, capture_height={capture_height}, is_desktop_handle={is_desktop_handle}")

        # 创建设备上下文并分配资源
        hwndDC = win32gui.GetWindowDC(hwnd)
        if hwndDC:
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, capture_width, capture_height)
            saveDC.SelectObject(saveBitMap)

            # 执行屏幕截图
            saveDC.BitBlt((0, 0), (capture_width, capture_height), mfcDC, (x_offset, y_offset), win32con.SRCCOPY)
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)

            # img = Image.frombuffer(
            #     'RGB',
            #     (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            #     bmpstr, 'raw', 'BGRX', 0, 1)
            img = Image.frombytes(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)
        else:
            img = None
            log3.logger.error(f"创建设备上下文并分配资源失败 - hwndDC")

        return img

    except win32ui.error as e:
        log3.logger.error(f"{e} {traceback.format_exc()}")
        return None
    finally:
        if saveBitMap:
            try:
                win32gui.DeleteObject(saveBitMap.GetHandle())
            except Exception as e:
                pass
                # print(f"Error releasing saveBitMap: {e}")
        if saveDC:
            try:
                saveDC.DeleteDC()
            except win32ui.error as e:
                pass
                # print(f"Error releasing saveDC: {e}")
        if mfcDC:
            try:
                mfcDC.DeleteDC()
            except win32ui.error as e:
                pass
                # print(f"Error releasing mfcDC: {e}")
        if hwndDC:
            try:
                win32gui.ReleaseDC(hwnd, hwndDC)
            except win32gui.error as e:
                pass
                # print(f"Error releasing hwndDC: {e}")


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
                # log3.logger.info(f"找到匹配项={template_img_path}，位置: {pt}，大小: ({int(w * scale)}, {int(h * scale)})")

                del screen_gray
                del template
                return pt  # 返回匹配的坐标

    # print(f"未找到匹配项={template_img_path}")
    log3.logger.debug(f"未找到匹配项={template_img_path}")
    del screen_gray
    del template

    return None


# 工具函数：查找图像并返回坐标（坐标需要加上偏移的 x,y）
def find_image_in_window(hwnd, template_img_path, x_offset=0, y_offset=0, capture_width=None,
                         capture_height=None, threshold=0.7, is_desktop_handle=False):
    if hwnd is None:
        return None

    if not win32gui.IsWindow(hwnd):
        return None

    # 截取游戏窗口的图像（限制范围）
    screen_img = capture_window(hwnd, x_offset, y_offset, capture_width, capture_height, is_desktop_handle)

    # 检查图像的有效性
    if screen_img is None or screen_img.size[0] == 0 or screen_img.size[1] == 0:
        log3.logger.error(f"{hwnd} 截图无效 - {template_img_path} {x_offset} {y_offset} {capture_width} {capture_height}")
        return None

    # 使用多尺度模板匹配，并获取匹配的坐标
    match_location = multi_scale_template_matching(screen_img, template_img_path, threshold)
    # 显示结果
    # cv2.imshow("Result", np.array(screen_img))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    try:
        if None is not screen_img:
            screen_img.close()
            del screen_img
    except Exception as e:
        print(f"{e} = {traceback.format_exc()}")

    if match_location:
        return match_location  # 返回匹配坐标 (x, y)
    return None


# 示例用法
if __name__ == "__main__":
    window_name = "夏禹剑 - 刀剑2"  # 替换为你的游戏窗口名称
    template_img_path = "./img/dahuang.bmp"  # 替换为你要匹配的模板图片路径

    # hwnd = win_tool.get_window_handle(window_name)
    w, h = win_tool.get_win_w_h()
    hwnd = desktop_handle = win_tool.get_desktop_window_handle()

    # 设置截图范围，x_offset, y_offset, capture_width, capture_height
    match_location = find_image_in_window(hwnd, template_img_path, int(w*0.75), int(h*0.6), w, h)
    if match_location:
        print(f"图像匹配成功，坐标: {match_location}")
    else:
        print("图像匹配失败")
