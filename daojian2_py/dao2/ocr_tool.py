import cv2
from paddleocr import PaddleOCR
import bg_find_pic_area
import numpy as np
import win_tool


def capture_window_to_str(hwnd, x_f, y_f, w, h, target_line_sub_str = None, is_desktop_handle=False):
    image = bg_find_pic_area.capture_window(hwnd, x_f, y_f, w, h, is_desktop_handle)
    # 转为灰度图
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    # 使用 PaddleOCR 进行中文识别
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    result = ocr.ocr(gray_image, cls=True)
    # 输出识别结果
    res = ""
    for line in result[0]:
        print(f"文字: {line[1][0]}, 置信度: {line[1][1]:.2f}")
        if None is not target_line_sub_str:
            if target_line_sub_str in line[1][0]:
                return line[1][0]
        res = res + line[1][0]

    if None is not target_line_sub_str:
        return ""
    return res


if __name__ == "__main__":
    pass
    # window_name = "夏禹剑 - 刀剑2"
    # hwnd = win_tool.get_window_handle(window_name)
    #
    # w, h = win_tool.get_win_w_h()
    # str = capture_window_to_str(hwnd, int(w * 0.2), 0, int(w * 0.75), int(h * 0.7), "成长等级")
    # print(str)