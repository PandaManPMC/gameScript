import random
import time
import os


def randint(a, b):
    seed = int(time.time() * 1000) ^ os.getpid()
    random.seed(seed)
    return random.randint(a, b)


def rand_float(num=0.1, sigma=1.0, length=3):
    rand_num = random.gauss(num, sigma)
    return round(abs(rand_num), length)


# 一些游戏，对于按键频率进行检测，如果对休眠做随机处理，一定程度可以避免被检测
def rand_min_float(min_num=0.1):
    f = rand_float(0.1, 0.15, 2)
    if f > 1:
        f = f - 1
    print(round(min_num+f, 2))
    return round(min_num+f, 2)


# 数字最后出现的索引
def rfind_digit_inx(txt):
    # 遍历每个数字字符并查找最后出现的索引
    for digit in "0123456789":
        position = txt.rfind(digit)  # 从右查找数字
        if position > -1:
            return position
    return -1
