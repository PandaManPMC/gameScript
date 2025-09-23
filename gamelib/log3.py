from datetime import datetime

# coding=utf-8
import logging

logger = logging.getLogger("log3")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(filename)s[lineno:%(lineno)d]-%(levelname)s-%(message)s')

# 使用FileHandler输出到文件
fh = logging.FileHandler(filename='now.log', mode='a')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

# 使用StreamHandler输出到屏幕
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

# 添加两个Handler
logger.addHandler(ch)
logger.addHandler(fh)


def date():
    current_datetime = datetime.now()
    year = current_datetime.year
    month = current_datetime.month
    day = current_datetime.day
    hour = current_datetime.hour
    minute = current_datetime.minute
    second = current_datetime.second

    return f"{year}-{month}-{day} {hour}:{minute}:{second}"


def console(text):
    print(f"{date()}：{text}")
    logger.debug(f'{text}')


if __name__ == "__main__":
    console(1)