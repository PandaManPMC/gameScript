import time

import dao2_common
import win_tool
import ocr_tool
import log3
from tkinter import messagebox
import traceback


w, h = win_tool.get_win_w_h()

CENTER_X_OFFSET = int(w * 0.25)
CENTER_Y_OFFSET = int(0.32 * h)
CENTER_W = int(w * 0.67)
CENTER_H = int(h * 0.67)

is_run_qiang_hua = False

is_run_ren_zhu = False


# 只保留+10和+17 qianghua_btn
def run_qiang_hua(hwnd):
    global is_run_qiang_hua

    while is_run_qiang_hua:
        time.sleep(0.1)
        # 找强化按钮
        xy = dao2_common.find_pic(hwnd, "img/qianghua_btn.bmp", int(w * 0.1), int(h * 0.2), int(w * 0.55), int(h * 0.9), 0.8)
        if None is xy:
            dao2_common.say_hwnd(hwnd, "未找到强化按钮，请打开装备强化界面")
            time.sleep(3)
            continue
        # 点击强化
        win_tool.send_mouse_left_click(hwnd, xy[0] + 3, xy[1] + 3)
        time.sleep(0.45)
        # 进行 AI 识图
        s = ocr_tool.capture_window_to_str(hwnd, CENTER_X_OFFSET, CENTER_Y_OFFSET, CENTER_W, CENTER_H, ["本次强化效果", "之前强化效果"])
        log3.logger.info(s)
        s_arr = s.strip().split("\n")

        if 2 != len(s_arr):
            log3.logger.info(f"文字识别出现异常，放弃本次强化= {s}")
            is_run_qiang_hua = False
            messagebox.showwarning("警告", f"强化失败{s}，不要调整强化结果窗口位置，检查强化材料是否足够。")
            return

        log3.logger.info(f"s_arr={s_arr}")
        try:
            current = int(s_arr[0].split("：")[1].strip())
            last = int(s_arr[1].split("：")[1].strip())
            log3.logger.info(f"本次强化+{current},上次强化+{last}")

            for _ in range(3):
                # 只保留 +17 + 10 和比上次高
                if current > last:
                    xy = dao2_common.find_pic(hwnd, "img/btn_gouzi.bmp", int(w * 0.2), int(0.15 * h), int(w * 0.75), int(h * 0.8), 0.8)
                    if None is xy:
                        time.sleep(0.3)
                        continue
                    # 点击保存 完成这个槽位的强化
                    win_tool.send_mouse_left_click(hwnd, xy[0] + 3, xy[1] + 5)

                    if 17 == current:
                        dao2_common.say_hwnd(hwnd, f"完成一次强化{current}")
                        return
                    elif 10 == current:
                        dao2_common.say_hwnd(hwnd, f"完成一次强化{current}")
                        return
                    break
                else:
                    # 不符合强化，点击不保存 btn_x
                    xy = dao2_common.find_pic(hwnd, "img/btn_x.bmp", int(w * 0.2), int(0.15 * h), int(w * 0.75), int(h * 0.8), 0.8)
                    if None is xy:
                        time.sleep(0.3)
                        continue
                    win_tool.send_mouse_left_click(hwnd, xy[0] + 3, xy[1] + 5)
                    break

        except Exception as e:
            log3.logger.error(traceback.format_exc())
            messagebox.showwarning("警告", f"强化异常{s}，请不要调整强化结果窗口的位置。")
            is_run_qiang_hua = False
            return


def run_ren_zhu(hwnd):
    global is_run_ren_zhu
    # 打开背包，找到装备的位置
    bag_xy = None
    for _ in range(5):
        bag_xy = dao2_common.find_pic(hwnd, "img/dakai_debeibao.bmp", int(w * 0.1), 0, w-200, int(h * 0.5), 0.8)
        if None is bag_xy:
            dao2_common.open_bag(hwnd)
            time.sleep(0.35)
            continue
        break

    if None is bag_xy:
        messagebox.showwarning("警告", f"背包定位失败")
        is_run_ren_zhu = False
        return

    # 按 2 认主
    r_z_xy = dao2_common.find_pic(hwnd, "img/renzhu_kuaijie2.bmp", int(w * 0.2), int(h * 0.7), int(w * 0.7), h - 20, 0.8)
    if None is r_z_xy:
        win_tool.send_key_to_window_frequency(hwnd, "1", 1)
        time.sleep(0.35)
    r_z_xy = dao2_common.find_pic(hwnd, "img/renzhu_kuaijie2.bmp", int(w * 0.2), int(h * 0.7), int(w * 0.7), h - 20, 0.8)
    if None is r_z_xy:
        messagebox.showwarning("警告", f"未找到认主技能，请放在快捷键 2 位置")
        is_run_ren_zhu = False
        return

    # 2k 下的第一个点
    f_x = bag_xy[0] + 27
    f_y = bag_xy[1] + 64
    # 偏移
    if 1920 == w:
        # 1080p 处理
        f_x = bag_xy[0] + int(27 * 0.75)
        f_y = bag_xy[1] + int(64 * 0.75)

    time.sleep(0.1)
    dao2_common.say_hwnd(hwnd, f"开始认主 保留733... 背包定位={f_x} , {f_y}")

    # 开始认主
    while is_run_ren_zhu:
        time.sleep(0.2)

        r_z_xy = dao2_common.find_pic(hwnd, "img/renzhu_kuaijie2.bmp", int(w * 0.2), int(h * 0.7), int(w * 0.7), h - 20,0.8)
        if None is r_z_xy:
            win_tool.send_key_to_window_frequency(hwnd, "1", 1)
            time.sleep(0.35)

        win_tool.send_key_to_window_frequency(hwnd, "2", 1)
        time.sleep(0.2)
        win_tool.send_mouse_left_click(hwnd, f_x, f_y)
        time.sleep(0.1)
        # 把鼠标移走
        win_tool.move_mouse_to(hwnd, 0, 0)
        time.sleep(0.3)

        try:
            # 认主识字
            s_arr = ocr_tool.capture_window_to_str(hwnd, CENTER_X_OFFSET, CENTER_Y_OFFSET, CENTER_W, CENTER_H, ["认主后会对该道具进行绑定", "本次为第"])
            s_arr = s_arr.strip().split("\n")
            log3.logger.info(f"认主识字={s_arr}")

            if 1 != len(s_arr) or "" == s_arr[0]:
                is_run_ren_zhu = False
                messagebox.showwarning("警告", f"认主识图无内容，{s_arr}")
                return

            if "认主后会对该道具进行绑定" in s_arr[0]:
                # 确定绑定
                xy = dao2_common.find_pic(hwnd, "img/btn_gouzi.bmp", int(w * 0.2), int(0.2 * h), int(w * 0.75),
                                          int(h * 0.8), 0.8)
                if None is xy:
                    is_run_ren_zhu = False
                    messagebox.showwarning("警告", f"未找到确定绑定按钮")
                    return
                win_tool.send_mouse_left_click(hwnd, xy[0] + 3, xy[1] + 5)
                time.sleep(0.4)
                s_arr = ocr_tool.capture_window_to_str(hwnd, CENTER_X_OFFSET, CENTER_Y_OFFSET, CENTER_W, CENTER_H,
                                                       ["本次为第"])
                s_arr = s_arr.strip().split("\n")
                log3.logger.info(f"认主识字={s_arr}")

            if "" == s_arr[0]:
                dao2_common.say_hwnd(hwnd, f"认主可能已经完成")
                time.sleep(1)
                # messagebox.showwarning("警告", f"认主可能已经完成")
                is_run_ren_zhu = False
                return

            s2 = s_arr[0].strip().split("【")
            print(f"s2={s2}")
            count_s = s2[1].split("】")
            print(count_s)
            count = int(count_s[0].strip())

            num_s = s2[2].split("】")
            num = int(num_s[0].strip())
            log3.logger.info(f"认主次数={count}, 认主点数={num}")

            is_btn = False
            for _ in range(3):
                if (1 == count and 7 == num) or (1 < count and 3 == num):
                    log3.logger.info(f"保存本次认主 认主次数={count}, 认主点数={num}")
                    # 保存
                    xy = dao2_common.find_pic(hwnd, "img/btn_gouzi.bmp", int(w * 0.2), int(0.2 * h), int(w * 0.75),
                                              int(h * 0.8), 0.8)
                    if None is xy:
                        time.sleep(0.15)
                        continue
                    win_tool.send_mouse_left_click(hwnd, xy[0] + 3, xy[1] + 5)
                    time.sleep(0.4)
                    is_btn = True
                    dao2_common.say_hwnd(hwnd, f"第 {count} 次认主，保存 {num}")
                    break
                else:
                    # 取消本次认主
                    xy = dao2_common.find_pic(hwnd, "img/btn_x.bmp", int(w * 0.2), int(0.15 * h), int(w * 0.75), int(h * 0.8),
                                              0.8)
                    if None is xy:
                        time.sleep(0.15)
                        continue
                    win_tool.send_mouse_left_click(hwnd, xy[0] + 3, xy[1] + 5)
                    is_btn = True
                    break

            if not is_btn:
                # 没有按钮，可能已经认主完成
                messagebox.showwarning("警告", f"认主可能已经完成")
                is_run_ren_zhu = False
                return

        except Exception as e:
            log3.logger.error(f"{traceback.format_exc()}")
            dao2_common.say_hwnd(hwnd, f"认主失败 {e}")
            time.sleep(0.3)
            messagebox.showwarning("警告", f"认主出现异常")
            is_run_ren_zhu = False
            return