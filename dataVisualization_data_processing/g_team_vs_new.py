import pandas as pd
from datetime import datetime
import numpy as np


def convert_duration_to_minutes(duration_str):
    """
    将不同格式的时长字符串转换为分钟数（保留一位小数）
    """
    parts = duration_str.split(':')
    if len(parts) == 3:
        minutes = float(parts[0])
        seconds = float(parts[1])
    elif len(parts) == 2:
        minutes = float(parts[0])
        seconds = float(parts[1])
    else:
        raise ValueError(f"Unexpected duration format: {duration_str}")

    return round(minutes + seconds / 60, 1)


def calculate_team_player_stats(matches, team_prefix):
    """
    计算队伍所有选手的总体数据
    """
    total_stats = {
        'kills': 0,
        'deaths': 0,
        'assists': 0,
        'CS': 0,
        'gold': 0.0,
        'damage': 0.0,
        'tanking': 0.0
    }

    for player_num in range(1, 6):
        total_stats['kills'] += matches[f'{team_prefix}_player{player_num}_K'].sum()
        total_stats['deaths'] += matches[f'{team_prefix}_player{player_num}_D'].sum()
        total_stats['assists'] += matches[f'{team_prefix}_player{player_num}_A'].sum()
        total_stats['CS'] += matches[f'{team_prefix}_player{player_num}_CS'].sum()
        total_stats['gold'] += matches[f'{team_prefix}_player{player_num}_gold'].sum()
        total_stats['damage'] += matches[f'{team_prefix}_player{player_num}_damage'].sum()
        total_stats['tanking'] += matches[f'{team_prefix}_player{player_num}_tanking'].sum()

    return total_stats


def process_team_vs_data(input_file, output_file):
    """
    处理队伍对位宏观数据并生成统计报告
    """
    # 读取CSV文件
    df = pd.read_csv(input_file)

    # 转换Duration为分钟
    df['Minutes'] = df['Duration'].apply(convert_duration_to_minutes)

    # 存储处理后的数据
    processed_data = []

    # 按赛段分组处理数据
    for match_type, match_type_group in df.groupby('matchType'):
        # 获取该赛段中所有唯一的队伍对
        unique_teams = set()
        for _, row in match_type_group.iterrows():
            # 使用tuple sorted确保队伍对的唯一性
            team_pair = tuple(sorted([
                (row['Team1'], row['Team1_region']),
                (row['Team2'], row['Team2_region'])
            ]))
            unique_teams.add(team_pair)

        # 处理每对队伍
        for (team1, region1), (team2, region2) in unique_teams:
            # 获取这两支队伍的所有比赛
            team_matches = match_type_group[
                ((match_type_group['Team1'] == team1) & (match_type_group['Team2'] == team2)) |
                ((match_type_group['Team1'] == team2) & (match_type_group['Team2'] == team1))
                ]

            # 初始化基础数据
            vs_data = {
                'Team1_name': team1,
                'Team1_region': region1,
                'Team2_name': team2,
                'Team2_region': region2,
                'matchType': match_type,
                'matches_played': len(team_matches),
                'minutes_played': round(team_matches['Minutes'].sum(), 1)
            }

            # 处理每个队伍的数据
            for team_idx, (team, region) in enumerate([(team1, region1), (team2, region2)], 1):
                team_prefix = f'Team{team_idx}'

                # 处理资源数据
                team_matches_as_team1 = team_matches[team_matches['Team1'] == team]
                team_matches_as_team2 = team_matches[team_matches['Team2'] == team]

                # 计算客观资源数据
                vs_data[f'{team_prefix}_Baron'] = (
                        team_matches_as_team1['Team1_Baron'].sum() +
                        team_matches_as_team2['Team2_Baron'].sum()
                )
                vs_data[f'{team_prefix}_Dra'] = (
                        team_matches_as_team1['Team1_Dra'].sum() +
                        team_matches_as_team2['Team2_Dra'].sum()
                )
                vs_data[f'{team_prefix}_Turts'] = (
                        team_matches_as_team1['Team1_Turts'].sum() +
                        team_matches_as_team2['Team2_Turts'].sum()
                )

                # 计算胜场数
                vs_data[f'matches_won_{team_idx}'] = len(team_matches[team_matches['win'] == team])

                # 计算选手总体数据
                stats_as_team1 = calculate_team_player_stats(team_matches_as_team1, 'Team1')
                stats_as_team2 = calculate_team_player_stats(team_matches_as_team2, 'Team2')

                # 合并数据
                vs_data[f'{team_prefix}_kills'] = stats_as_team1['kills'] + stats_as_team2['kills']
                vs_data[f'{team_prefix}_deaths'] = stats_as_team1['deaths'] + stats_as_team2['deaths']
                vs_data[f'{team_prefix}_assists'] = stats_as_team1['assists'] + stats_as_team2['assists']
                vs_data[f'{team_prefix}_CS'] = stats_as_team1['CS'] + stats_as_team2['CS']
                vs_data[f'{team_prefix}_gold'] = round(stats_as_team1['gold'] + stats_as_team2['gold'], 1)
                vs_data[f'{team_prefix}_damage'] = round(stats_as_team1['damage'] + stats_as_team2['damage'], 1)
                vs_data[f'{team_prefix}_tanking'] = round(stats_as_team1['tanking'] + stats_as_team2['tanking'], 1)

            processed_data.append(vs_data)

    # 创建结果DataFrame
    result_df = pd.DataFrame(processed_data)

    # 确保整数类型的列
    integer_columns = [
        'Team1_Baron', 'Team1_Dra', 'Team1_Turts',
        'Team2_Baron', 'Team2_Dra', 'Team2_Turts',
        'Team1_kills', 'Team1_deaths', 'Team1_assists', 'Team1_CS',
        'Team2_kills', 'Team2_deaths', 'Team2_assists', 'Team2_CS',
        'matches_played', 'matches_won_1', 'matches_won_2'
    ]
    for col in integer_columns:
        result_df[col] = result_df[col].astype(int)

    # 保存结果
    result_df.to_csv(output_file, index=False, encoding='utf-8')


# 使用函数
process_team_vs_data('ori.csv', '04_team_vs_new.csv')