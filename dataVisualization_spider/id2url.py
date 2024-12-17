import pandas as pd

# 读取CSV文件
def read_csv(file_path):
    return pd.read_csv(file_path)

# 生成未出现的matchid和对应的URL
def generate_notexist_id_url(matchid_list):
    notexist_ids = []
    for matchid in range(1, 100001):
        if matchid not in matchid_list:
            notexist_ids.append({'MatchID': matchid, 'URL': f'https://www.wanplus.cn/schedule/{matchid}.html'})
    return pd.DataFrame(notexist_ids)

# 主函数
def main():
    # 假设CSV文件路径为'cleaned_output.csv'
    file_path = 'data2/cleaned_output.csv'
    
    # 读取CSV文件
    df = read_csv(file_path)
    
    # 获取matchid列
    matchid_list = df['MatchID'].dropna().astype(int).tolist()
    
    # 生成未出现的matchid和对应的URL
    notexist_df = generate_notexist_id_url(matchid_list)
    
    # 如果未出现的matchid和URL不为空，则保存到CSV文件
    if not notexist_df.empty:
        notexist_df.to_csv('notexist_id_url.csv', index=False, encoding='utf-8')
    else:
        print("所有matchid都已存在，无需生成新文件。")

if __name__ == '__main__':
    main()