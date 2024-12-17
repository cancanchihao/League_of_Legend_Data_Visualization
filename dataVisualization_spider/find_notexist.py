import pandas as pd

# 读取CSV文件
def read_csv(file_path):
    return pd.read_csv(file_path)

# 检查并保存不存在的MatchID
def save_nonexistent_matchids(df1, df2, output_file):
    # 合并两个DataFrame的MatchID列到一个集合中
    existing_ids = set(df1['MatchID']).union(set(df2['MatchID']))
    
    # 创建一个包含1到100000的数字的序列
    nonexistent_ids = [i for i in range(1, 100001) if i not in existing_ids]
    
    # 将不存在的MatchID保存到CSV文件
    pd.DataFrame(nonexistent_ids, columns=['MatchID']).to_csv(output_file, index=False)

# 主函数
def main():
    # 假设sorted_merged_output.csv和sorted_error_log.csv文件路径
    input_file_path1 = 'sorted_merged_output.csv'
    input_file_path2 = 'sorted_error_log.csv'
    output_file_path = 'noexist.csv'
    
    # 读取两个CSV文件
    df1 = read_csv(input_file_path1)
    df2 = read_csv(input_file_path2)
    
    # 检查并保存不存在的MatchID
    save_nonexistent_matchids(df1, df2, output_file_path)

    print(f"完成检查，不存在的MatchID已保存到{output_file_path}")

if __name__ == '__main__':
    main()