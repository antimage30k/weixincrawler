import random
import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # strftime 把 unix time 转换为日常看到的格式
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(formatted, *args, **kwargs)
        print(formatted, *args, file=f, **kwargs)


def formatted_time(time_stamp):
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time_stamp))
    formatted = time.strftime(time_format, localtime)
    return formatted


def validate_title(title):
    # valid_title = ''
    # illegal = '/\:*?"<>|'
    # for i in title:
    #     if i in illegal:
    #         i = '_'
    #     valid_title += i
    # return valid_title
    illegal = '/\:*?"<>|'
    trans = '_________'
    table = str.maketrans(illegal, trans)
    return title.translate(table)