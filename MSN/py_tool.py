import random
import time
import os


def randint(a, b):
    seed = int(time.time() * 1000) ^ os.getpid()
    random.seed(seed)
    return random.randint(a, b)


# 数字最后出现的索引
def rfind_digit_inx(txt):
    # 遍历每个数字字符并查找最后出现的索引
    for digit in "0123456789":
        position = txt.rfind(digit)  # 从右查找数字
        if position > -1:
            return position
    return -1
