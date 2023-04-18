import pandas as pd

file_name = "output.csv"  # 指定文件名
df = pd.read_csv(file_name,encoding="utf-8")  # 读取csv文件到DataFrame对象中
df.drop_duplicates(keep='first', inplace=True)  # 删除重复行，只保留第一次出现的
# 将处理后的数据重新写回到原文件中
df.to_csv(file_name, index=False)
a = input("去重完成！按任意键退出")