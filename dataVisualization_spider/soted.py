import pandas as pd

# 读取CSV文件
def read_csv(file_path):
    return pd.read_csv(file_path)

# 按MatchID和可选的gameset排序
def sort_by_matchid_and_gameset(df):
    # 确保MatchID列存在
    if 'MatchID' not in df.columns:
        raise ValueError("CSV文件中没有名为'MatchID'的列")

    # 检查gameset列是否存在
    if 'gameset' in df.columns and df['gameset'].notnull().any():
        # 如果gameset列存在且至少有一个非空值，按照MatchID和gameset进行排序
        sorted_df = df.sort_values(by=['MatchID', 'gameset'], ascending=[True, True])
    else:
        # 如果gameset列不存在或全部为空，只按照MatchID进行排序
        sorted_df = df.sort_values(by='MatchID', ascending=True)
    
    return sorted_df

# 主函数
def main():
    # 假设CSV文件路径为'cleaned_output.csv'
    file_path = 'cleaned_output.csv'
    
    # 读取CSV文件
    df = read_csv(file_path)
    
    # 按照MatchID和gameset排序
    sorted_df = sort_by_matchid_and_gameset(df)
    
    # 打印排序后的结果
    print(sorted_df)

    # 可以选择将排序后的结果保存为新的CSV文件
    sorted_df.to_csv('sorted_cleaned_output.csv', index=False)

if __name__ == '__main__':
    main()