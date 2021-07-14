import numpy as np 
import pandas as pd 
import time
import math
    
def add_time(df):#遍历行，读取时间的行，并把这个值作为下8行的时间属性赋值
    temptime = 0
    i = 0
    while i<len(df):
        if int(df.iloc[i]['a'])>8:#如果是时间那一行
            temptime = int(df.iloc[i]['a'])
        else:
            df.loc[i,'time'] = temptime#如果是水位的行，就把最近读取的那个时间赋上去
        i=i+1
    


if __name__ == '__main__':
    #在这个操作前手动把csv前两行删掉并添加“a,b”作为第一行,当然最好是写上对应的属性名：站点，水位更好一些，我这里图省事就先用ab代替了。
    PATH = "E:\\CODE\\PY\\hsk_datatrans\\fort.txt.csv"
    data = pd.read_csv(PATH,encoding = 'utf-8')#读取csv文件
    print(data.head(10))
    data['time']='0'#添加一个新的列属性‘time’
    print(data.head(10))
    add_time(data)
    print(data.head(20))
    data = data.loc[lambda df:df.a<9,:]#只保留a列小于9的，也就是说把原来的时间行删掉
    print(data.head(20))

    #到这里data已经包含所有数据并能方便调取，每行包含站点，水位，时间。
    #下面是调用部分数据的例子：只调取站点序号为1的数据：
    data1 = data.loc[lambda df:df.a==1,:]#只保留a列==1的数据
    print(data1.head(20))
    data1.to_csv(PATH+'data1.csv')#保存csv文件
