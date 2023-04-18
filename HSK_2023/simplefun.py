import csv
from datetime import datetime
import os

def message_box(txt):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = str(current_time) + ': ' + str(txt)
    with open('error_log.txt', 'a', encoding="utf-8") as file:
        file.write(message + '\n')


def filterlist(elelist):
    if not os.path.exists("done.txt"):
        return elelist
    with open("done.txt", "r",encoding="utf-8") as f:
        done_str = f.read().strip()  # 读取done.txt中的文本内容并去除首尾空格

    done_list = done_str.split(",")  # 将用逗号分隔的字符串转换为列表

    # 删除elelist中包含在done_list中的元素
    for item in done_list:
        if item in elelist:
            elelist.remove(item)
    return elelist


def writelist(lists):
    with open("shuiwenzhan.txt", "w", encoding="utf-8") as f:
        for i in range(len(lists)):
            if i > 0:
                f.write(",")
            f.write(lists[i])
    message_box("结果已保存至shuiwenzhan.txt文件中！")


def writecsv(line):
    with open('output.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(line)