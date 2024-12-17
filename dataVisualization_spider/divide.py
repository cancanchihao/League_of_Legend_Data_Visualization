import os
import shutil
import pandas as pd

# 定义文件路径
txt_path = r'D:\MyCode\PYTHON\dataVisualization\赛段.txt'
csv_path = r'D:\MyCode\PYTHON\dataVisualization\data2\sorted_cleaned_output.csv'
logo_folder_path = r'D:\MyCode\PYTHON\dataVisualization\team_img'
output_folder_path = r'D:\MyCode\PYTHON\dataVisualization\matchType_devide'

# 读取赛段名称
with open(txt_path, 'r', encoding='utf-8') as file:
    stages = [line.strip().replace(' ', '') for line in file.readlines()]

print(stages)

# 创建输出文件夹
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 使用pandas读取csv文件
df = pd.read_csv(csv_path)

df['matchType'] = df['matchType'].str.replace(' ', '', regex=False)


print(df['matchType'])

# 读取csv文件并查找队伍
stages_teams = {stage: set() for stage in stages}
for stage in stages:
    # 过滤出当前赛段的数据
    stage_df = df[df['matchType'] == stage]
    for index, row in stage_df.iterrows():
        stages_teams[stage].add(row['Team1'])
        stages_teams[stage].add(row['Team2'])

# 复制logo图片到新的文件夹
for stage, teams in stages_teams.items():
    stage_folder_path = os.path.join(output_folder_path, stage)
    if not os.path.exists(stage_folder_path):
        os.makedirs(stage_folder_path)
    
    for team in teams:
        # 假设logo文件名与队伍名称相同，这里需要根据实际情况调整
        team_logo_path = os.path.join(logo_folder_path, f'{team}.png')
        if os.path.exists(team_logo_path):
            shutil.copy(team_logo_path, stage_folder_path)

# 打印每个赛段的队伍信息
for stage, teams in stages_teams.items():
    print(f'赛段：{stage}, 队伍：{teams}')