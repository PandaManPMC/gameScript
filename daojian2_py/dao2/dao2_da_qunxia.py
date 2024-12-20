import win_tool
import threading
import time
import dao2_common
import traceback
from tkinter import messagebox
from datetime import datetime
import log3

w, h = win_tool.get_win_w_h()

is_run = False
lock = threading.Lock()

run_hwnd = {}


def start_da_qun_xia(hwnd):
    global is_run
    with lock:

        # 不重复打
        if hwnd in run_hwnd:
            return
        else:
            run_hwnd[hwnd] = True

        if is_run:
            t = threading.Thread(target=da_qun_xia, args=(hwnd,), daemon=True)
            t.start()


def da_qun_xia(hwnd):
    global is_run
    start_time = time.time()

    # win_tool.activate_window(hwnd)
    # time.sleep(0.3)

    dao2_common.say_hwnd(hwnd, f"{hwnd} 开始打群侠 技能在 1 至 - 快捷栏")

    try:
        is_ok = dao2_common.tu_dun_wa_dang(hwnd)
    except Exception as e:
        print(f"发生异常：{e}")
        is_ok = traceback.format_exc()
        print(is_ok)

    if "" != is_ok:
        is_run = False
        messagebox.showwarning("警告", is_ok)
        return
    # 土遁后休息等逻辑同步
    time.sleep(9)

    # 刷一下逻辑同步
    if is_run is False:
        print("停止脚本")
        return
    time.sleep(0.3)
    win_tool.send_key_to_window_frequency(hwnd, "w", 3)

    time.sleep(1)

    # 第 个点开始是金陵
    jin_lin_inx = 3
    qun_xia = [["img/qunxia_chencang.bmp"],
               ["img/qunxia_gaochenfeng.bmp"],
               ["img/qunxia_sumei.bmp"],
               ["img/qunxia_wufanbao.bmp"],
               ["img/qunxia_rongjin.bmp"],
               ["img/qunxia_liupeng.bmp"],
               ["img/qunxia_tongbaiming.bmp"]]
    # qun_xia_tx = ["img/qunxia_chencang_tx.bmp", "img/qunxia_gaochengfeng_tx.bmp", "img/qunxia_sumei_tx.bmp",
    #            "img/qunxia_wufanbao_tx.bmp", "img/qunxia_rongjin_tx.bmp", "img/qunxia_liupen_tx.bmp",
    #               "童百明"]
    qun_xia_tx = ["陈仓", "高乘风", "苏媚",
                  "吴范保", "荣金", "刘鹏",
                  "童百明"]
    # position = ["673,553", "630,468", "630,452",
    #             "2139,2760", "2079,2755", "2182,2673", ""]
    position = ["", "", "",
                "", "", "", ""]
    # camera_model = [1, 1, 1,
    #                 1, 2, 1, 0]
    camera_model = [0, 0, 0,
                    0, 0, 0, 0]
    delay = [12, 10, 6,
             12, 8, 12, 3]
    # 技能
    skill = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-"]

    for inx in range(len(qun_xia)):

        # 金陵
        if inx == jin_lin_inx:
            dao2_common.tu_dun_jin_lin(hwnd)
            time.sleep(10)
            win_tool.send_key_to_window_frequency(hwnd, "w", 3)
            time.sleep(3)

        # 找图
        for i in range(5):
            if is_run is False:
                print("停止脚本")
                return

            # 导航
            on_xy = None
            if "" != position[inx]:
                on_xy = dao2_common.navigation_x_y(hwnd, position[inx])

            else:
                on_xy = dao2_common.navigation_name(hwnd, qun_xia[inx][0])

            if isinstance(on_xy, str):
                messagebox.showwarning("警告", on_xy)
                del run_hwnd[hwnd]
                return

            if 0 == i:
                # 骑马
                dao2_common.qi_ma(hwnd)
                time.sleep(delay[inx])
            else:
                time.sleep(7)

            if is_run is False:
                print("停止脚本")
                return

            # 摆正相机
            if 0 == camera_model[inx]:
                print("不需要摆正相机")
            elif 1 == camera_model[inx]:
                dao2_common.camera_top(hwnd)
            else:
                dao2_common.camera_forward(hwnd)

            if is_run is False:
                print("停止脚本")
                return

            qx_xy = None
            if "" != position[inx]:
                for k in range(len(qun_xia[inx])):
                    qx_xy = dao2_common.find_pic(hwnd, qun_xia[inx][k], 400, 200, int(w * 0.7), int(h * 0.7), 0.7)
                    if None is not qx_xy:
                        break
                if None is qx_xy:
                    print(f"{hwnd} 未找到 {qun_xia[inx]}")
                    time.sleep(1)
                    continue

            o_x = 3
            o_y = 60
            is_find_tx = False
            for j in range(5):
                if is_run is False:
                    print("停止脚本")
                    return
                if "" == position[inx]:
                    is_find_tx = True
                    break

                # win_tool.send_input_mouse_right_click(qx_xy[0] + o_x, qx_xy[1] + o_y)
                win_tool.send_mouse_left_click(hwnd, qx_xy[0] + o_x, qx_xy[1] + o_y)
                time.sleep(0.3)

                xy2 = dao2_common.find_pic(hwnd, qun_xia_tx[inx], 300, 0, w - 50, int(h * 0.3))
                if None is xy2:
                    time.sleep(1)
                    o_x += 1
                    o_y += 6
                    continue
                is_find_tx = True

            # 没找到头像，找群侠失败
            if not is_find_tx:
                # is_run = False
                # messagebox.showwarning("警告", f"未找到{qun_xia[inx]}")
                # 找不到群侠，本次不作数
                continue

            # 左键点击群侠
            is_battle = False
            for j in range(3):
                if is_run is False:
                    print("停止脚本")
                    return

                if "" != position[inx]:
                    # win_tool.send_input_mouse_left_click(qx_xy[0] + o_x, qx_xy[1] + o_y)
                    win_tool.send_mouse_left_click(hwnd, qx_xy[0] + o_x, qx_xy[1] + o_y)
                    time.sleep(0.3)
                xy2 = dao2_common.find_pic(hwnd, "img/qunxia_biwuqiujiu.bmp", 400, int(h * 0.5), w - 300, h - 100, 0.8)
                if None is xy2:
                    time.sleep(1)
                    continue
                # win_tool.send_input_mouse_left_click(xy2[0] + 5, xy2[1] + 5)
                win_tool.send_mouse_left_click(hwnd, xy2[0] + 5, xy2[1] + 5)
                time.sleep(0.5)

                xy2 = dao2_common.find_pic(hwnd, "img/qunxia_queding.bmp", 400, int(h * 0.5), w - 300, h - 100, 0.8)
                if None is xy2:
                    time.sleep(1)
                    continue
                # win_tool.send_input_mouse_left_click(xy2[0] + 5, xy2[1] + 5)
                win_tool.send_mouse_left_click(hwnd, xy2[0] + 5, xy2[1] + 5)
                time.sleep(0.5)

                is_zhuwei = False
                for zw in range(3):
                    xy2 = dao2_common.find_pic(hwnd, "img/qunxia_qunxiazhuwei.bmp", 400, 100, w - 400, int(h * 0.6))
                    if None is xy2:
                        time.sleep(1)
                        continue
                    is_zhuwei = True
                # 没有群侠助威，说明已经打完了
                if not is_zhuwei:
                    break

                is_yi_di_tu = False
                for _ in range(3):
                    # win_tool.send_input_mouse_left_click(xy2[0] + 55, xy2[1] + 135)
                    win_tool.send_mouse_left_click(hwnd, xy2[0] + 55, xy2[1] + 135)
                    time.sleep(4)
                    is_battle = True
                    xy = dao2_common.find_pic(hwnd, "img/yiditu.bmp", 1000, 600, w, h)
                    if None is xy:
                        continue
                    # 开打，打断循环
                    is_yi_di_tu = True
                    break
                if is_yi_di_tu:
                    break
                else:
                    print("不在副本")
                    messagebox.showwarning("警告", "未找到 yiditu.bmp！")
                    is_run = False
                    return

            if not is_battle:
                break
            begin = time.time()

            # 进入副本,向前走3s，开始 tab 和 放技能
            dao2_common.camera_forward(hwnd)
            time.sleep(0.3)
            # win_tool.send_press_key("w", 2)
            win_tool.send_key_to_window(hwnd, "w", 2)

            # 开始战斗
            is_finish = False
            while is_run:
                dao2_common.activity_window(hwnd)
                for skill_index in range(len(skill)):
                    if not is_run:
                        break
                    # tab
                    win_tool.send_key_to_window(hwnd, "tab")
                    time.sleep(0.1)

                    if skill_index != 0 and skill_index % 4 == 0:
                        # win_tool.send_key("w", 3)
                        win_tool.send_key_to_window_frequency(hwnd, "w", 3)
                        time.sleep(0.5)

                    # 按键
                    win_tool.send_key_to_window(hwnd, skill[skill_index])
                    time.sleep(0.5)
                    skill_index += 1
                    time.sleep(0.4)

                    if 0 != skill_index and skill_index % 5 == 0:
                        xy2 = dao2_common.find_pic(hwnd, "img/qunxia_wanchengqueding.bmp", 400, int(h * 0.3), int(w * 0.7),
                                                   int(h * 0.7), 0.8)
                        if None is not xy2:
                            is_finish = True
                            # win_tool.send_input_mouse_left_click(xy2[0] + 3, xy2[1] + 3)
                            win_tool.send_mouse_left_click(hwnd, xy2[0] + 3, xy2[1] + 3)
                            time.sleep(3)
                            break
                if is_finish:
                    break

                xy = dao2_common.find_pic(hwnd, "img/yiditu.bmp", 1000, 600, w, h)
                if None is xy:
                    is_finish = True
                    break

            # 高级礼物
            time.sleep(3)
            xy2 = dao2_common.find_pic(hwnd, "img/qunxia_gaojiliwu.bmp", 400, int(h * 0.3), int(w * 0.7),
                                       int(h * 0.7))
            if None is not xy2:
                # win_tool.send_input_mouse_left_click(xy2[0] + 3, xy2[1] + 3)
                win_tool.send_mouse_left_click(hwnd, xy2[0] + 3, xy2[1] + 3)

            time.sleep(0.3)

            if is_finish:
                print(f"完成挑战 {qun_xia_tx[inx]} 耗时={time.time() - begin}")
                # dao2_common.say(f"完成群侠挑战 {qun_xia_tx[inx]} 耗时={time.time() - begin}")
                dao2_common.say_hwnd(hwnd, f"完成群侠挑战 {qun_xia_tx[inx]} 耗时={time.time() - begin}")
                # log3.logger.info(f"完成群侠挑战 {qun_xia_tx[inx]} 耗时={time.time() - begin}")

    del run_hwnd[hwnd]
    if 0 == len(run_hwnd):
        is_run = False
    dao2_common.say_hwnd(hwnd, f"{hwnd} 完成群侠挑战 耗时={time.time() - start_time}")
