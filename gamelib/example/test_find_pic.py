import numpy as np
import gamelib
import cv2


print(cv2.__version__)

if __name__ == "__main__":
    # test()
    w,h = gamelib.win_tool.get_win_w_h()
    window_handles = gamelib.win_tool.get_all_window_handles_by_name("37山河图志")
    print(window_handles)
    hwnd = window_handles[0]

    screen_img = gamelib.find_pic.capture_window_area(hwnd, 100, 200, w,h)
    cv2.imshow("Result", np.array(screen_img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
