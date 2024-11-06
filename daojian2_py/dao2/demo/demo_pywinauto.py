from pywinauto import application, mouse, keyboard
from pywinauto import findwindows
import time

# 获取所有窗口
windows = findwindows.find_elements()

win_name = "刀剑2"
process_id = 0

# 打印所有窗口的标题
for w in windows:
    print(f"Window Title: {w.name}")
    if win_name in w.name:
        win_name = w.name
        process_id = w.process_id
        break


# 连接到已经启动的程序，通过程序的标题连接
app = application.Application().connect(process=process_id)

# 获取窗口句柄（hwnd）
window = app.window(title=win_name)

# 获取窗口的矩形 (获取窗口位置和尺寸)
# rect = window.rectangle()

# 获取窗口坐标 (例如，窗口的左上角坐标)
# print(f"Window Position: {rect.left}, {rect.top}")

# 指定窗口内的相对坐标
x, y = 500, 500  # 假设目标位置是 (300, 200)

# 将相对坐标转换为屏幕坐标
# absolute_x = rect.left + x
# absolute_y = rect.top + y

# 移动鼠标到指定位置
# mouse.move([absolute_x, absolute_y])
# mouse.move([x, y])

# 等待1秒，确保鼠标悬停生效
time.sleep(3)

# 模拟鼠标点击
# mouse.click([absolute_x, absolute_y])
window.click_input(coords=(x, y), no_activate=True)

# 确保点击操作生效
time.sleep(1)
