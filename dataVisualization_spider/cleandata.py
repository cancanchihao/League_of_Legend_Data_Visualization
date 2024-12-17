import pandas as pd
import numpy as np

# 读取CSV文件
df = pd.read_csv('merged_output.csv')

# 删除包含空信息的数据行
df = df.replace('', np.nan)  # 将空字符串替换为np.nan
df = df.dropna(how='all')  # 删除所有列都是np.nan的行

# 删除包含"not_a_champ"的数据行
df = df[~df.apply(lambda row: row.astype(str).str.contains("not_a_champ").any(), axis=1)]

# 删除包含'no_ban'的数据行
df = df[~df.apply(lambda row: row.astype(str).str.contains("no_ban").any(), axis=1)]

# 删除包含np.nan的数据行
df = df.dropna()

# 保存清洗后的数据到新的CSV文件
df.to_csv('cleaned_output.csv', index=False, encoding='utf-8')