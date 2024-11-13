import cv2
from paddleocr import PaddleOCR
import bg_find_pic_area
import numpy as np
import win_tool
import log3
import traceback
import threading


LOCK_GLOBAL = threading.Lock()


ocr = None


def init_OCR():
    global ocr
    ocr = PaddleOCR(
        use_angle_cls=True,
        lang='ch',
        det_model_dir=win_tool.resource_path("paddle_ocr_models/det"),
        rec_model_dir=win_tool.resource_path("paddle_ocr_models/rec"),
        cls_model_dir=win_tool.resource_path("paddle_ocr_models/cls")
    )
    log3.logger.info(f"初始化 OCR {ocr}")


def capture_window_to_str(hwnd, x_f, y_f, w, h, target_line_sub_str = None, is_desktop_handle=False):
    global ocr

    with LOCK_GLOBAL:
        if None is ocr:
            init_OCR()

    image = bg_find_pic_area.capture_window(hwnd, x_f, y_f, w, h, is_desktop_handle)
    if None is image:
        return None

    # 转为灰度图
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    # 使用 PaddleOCR 进行中文识别
    # ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    result = ocr.ocr(gray_image, cls=True)
    # 输出识别结果
    res = ""
    try:
        # 1. 单个字符串
        if None is not target_line_sub_str and isinstance(target_line_sub_str, str):
            if None is result or None is result[0]:
                return ""
            for line in result[0]:
                print(f"{line[1][0]} 【】置信度: {line[1][1]:.2f}")
                if isinstance(target_line_sub_str, str):
                    if target_line_sub_str in line[1][0]:
                        return line[1][0]
        # 2.字符串数组
        elif None is not target_line_sub_str:
            for k in range(len(target_line_sub_str)):
                tag = target_line_sub_str[k]
                for line in result[0]:
                    if tag in line[1][0]:
                        res = res + "\n" + line[1][0]
                        break
        # 3.所有字符串
        else:
            for line in result[0]:
                print(f"{line[1][0]} 【】置信度: {line[1][1]:.2f}")
                res = res + "\n" + line[1][0]
    except Exception as e:
        log3.logger.error(f"{e} {traceback.format_exc()}")
    finally:
        image.close()

    return res


if __name__ == "__main__":
    pass
    init_OCR()

    window_name = "夏禹剑 - 刀剑2"
    hwnd = win_tool.get_window_handle(window_name)

    w, h = win_tool.get_win_w_h()
    # s = capture_window_to_str(hwnd, int(w * 0.2), 0, int(w * 0.75), int(h * 0.7), "成长等级")
    # s = capture_window_to_str(hwnd, int(w*0.5), 0, w, h)
    # s = capture_window_to_str(hwnd, int(w * 0.1), int(0.15 * h), int(w * 0.7), int(h * 0.8), "本次强化效果")
    # 本次为第【4】次认主，效果为：【2】，是
    # s_arr = capture_window_to_str(hwnd, 0, int(0.5 * h), int(w * 0.65), h, "获得刀币")
    # s_arr = s_arr.strip().split("\n")
    # print(s_arr)
    # f_inx = s_arr[0].find("获得刀币")
    # print(f_inx)
    # print(s_arr[0][:f_inx])
    s = capture_window_to_str(hwnd, int(w*0.2), int(h * 0.2), int(w*0.7), int(h * 0.7), "的坐骑")
    print(s)
    s = s.strip().split("\n")[0]
    print(s)
    s = s[0:s.find("]的坐骑")]
    print(s)
    if "[" == s[0]:
        s = s[1:]
    print(s)




