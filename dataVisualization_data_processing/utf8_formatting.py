import pandas as pd

# 读取之前处理过的 CSV 文件
df = pd.read_csv('07_hero_chosen_new - 副本.csv', encoding='gbk')


# 保存为新的 CSV 文件
df.to_csv('07_hero_chosen_new - 副本.csv', index=False, encoding='utf-8')

