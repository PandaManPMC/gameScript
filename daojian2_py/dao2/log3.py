from datetime import datetime


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


if __name__ == "__main__":
    console(1)