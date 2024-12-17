import pandas as pd
from datetime import datetime
import numpy as np


def convert_duration_to_minutes(duration_str):
    """
    将不同格式的时长字符串转换为分钟数（保留一位小数）
    支持两种格式：
    1. "分钟:秒:毫秒"
    2. "分钟:秒"
    """
    parts = duration_str.split(':')
    if len(parts) == 3:
        # 格式为 "分钟:秒:毫秒"
        minutes = float(parts[0])
        seconds = float(parts[1])
    elif len(parts) == 2:
        # 格式为 "分钟:秒"
        minutes = float(parts[0])
        seconds = float(parts[1])
    else:
        raise ValueError(f"Unexpected duration format: {duration_str}")

    # 将秒转换为分钟的小数部分（保留一位小数）
    return round(minutes + seconds / 60, 1)


def process_player_data(input_file, output_file):
    # 读取CSV文件
    df = pd.read_csv(input_file)

    # 用于存储处理后的数据
    processed_data = []

    ## 转换Duration为分钟（保留一位小数）
    df['Minutes'] = df['Duration'].apply(convert_duration_to_minutes)

    # 处理每支队伍的数据
    for team_num in [1, 2]:
        team_prefix = f'Team{team_num}'

        # 处理每个位置的选手
        for player_num in range(1, 6):
            # 获取基础列名
            name_col = f'{team_prefix}_player{player_num}_name'

            # 标准化选手名称（首字母大写，其他小写，去除空格）
            df[name_col] = df[name_col].str.strip().str.title()

            # 获取所有相关列
            base_cols = {
                'player_name': name_col,
                'team': df[team_prefix],
                'region': f'{team_prefix}_region',
                'position': player_num,
                'kills': f'{team_prefix}_player{player_num}_K',
                'deaths': f'{team_prefix}_player{player_num}_D',
                'assists': f'{team_prefix}_player{player_num}_A',
                'CS': f'{team_prefix}_player{player_num}_CS',
                'gold': f'{team_prefix}_player{player_num}_gold',
                'damage': f'{team_prefix}_player{player_num}_damage',
                'tanking': f'{team_prefix}_player{player_num}_tanking'
            }

            # 按matchType分组并聚合数据
            grouped = df.groupby(['matchType', base_cols['player_name'], base_cols['team'],
                                  df[base_cols['region']]])

            for group_key, group in grouped:
                matchType, player_name, team, region = group_key

                # 统计该选手在不同位置出现的次数
                position_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
                for _, row in group.iterrows():
                    # 通过检查所有player位置(1-5)找到当前选手在该行的位置编号
                    for pos in range(1, 6):
                        if row[f'{team_prefix}_player{pos}_name'] == player_name:
                            position_counts[pos] += 1
                            break

                # 找出出现次数最多的位置编号
                most_common_position = max(position_counts.items(), key=lambda x: x[1])[0]

                # 将位置编号映射为位置名称
                position_map = {1: 'TOP', 2: 'JUG', 3: 'MID', 4: 'ADC', 5: 'SUP'}
                position = position_map[most_common_position]

                # 汇总数据
                summary = {
                    'player_name': player_name,
                    'team': team,
                    'region': region,
                    'matchType': matchType,
                    'position': position,
                    'kills': group[base_cols['kills']].sum(),
                    'deaths': group[base_cols['deaths']].sum(),
                    'assists': group[base_cols['assists']].sum(),
                    'CS': group[base_cols['CS']].sum(),
                    'gold': round(group[base_cols['gold']].sum(), 1),
                    'damage': round(group[base_cols['damage']].sum(), 1),
                    'tanking': round(group[base_cols['tanking']].sum(), 1),
                    'matches_played': len(group),
                    'matches_won': len(group[group['win'] == team]),
                    'minutes_played': round(group['Minutes'].sum(), 1)  # 修改为保留一位小数
                }

                processed_data.append(summary)

    # 创建结果DataFrame并保存
    result_df = pd.DataFrame(processed_data)
    result_df.to_csv(output_file, index=False, encoding='utf-8')


# 使用函数
process_player_data('ori.csv', '02_player_new.csv')