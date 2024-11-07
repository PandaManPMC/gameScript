

# 数字最后出现的索引
def rfind_digit_inx(txt):
    # 遍历每个数字字符并查找最后出现的索引
    for digit in "0123456789":
        position = txt.rfind(digit)  # 从右查找数字
        if position > -1:
            return position
    return -1
