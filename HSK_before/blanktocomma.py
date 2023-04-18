PATH = "E:\\CODE\\PY\\hsk_datatrans\\fort.txt"

def deal_blank(PATH):# 把原文件中的连续空格转换成逗号，关键语法：split()
    ls = open(PATH).readlines()
    newTxt = ""
    for line in ls:
        newTxt = newTxt + ",".join(line.split()) + "\n"
    print(newTxt)

    fo = open(PATH+".csv", "x")#得到新文件csv格式，此格式适用于dataframe操作，更方便
    fo.write(newTxt)
    fo.close()

if __name__ == '__main__':
    deal_blank(PATH)