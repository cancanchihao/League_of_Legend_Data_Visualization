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
        minutes = float(parts[0])
        seconds = float(parts[1])
    elif len(parts) == 2:
        minutes = float(parts[0])
        seconds = float(parts[1])
    else:
        raise ValueError(f"Unexpected duration format: {duration_str}")

    return round(minutes + seconds / 60, 1)


def calculate_team_stats(df, team, team_position):
    """
    计算单个队伍在特定位置（Team1或Team2）的所有选手统计数据
    """
    prefix = f'Team{team_position}'
    stats = {
        'kills': 0,
        'deaths': 0,
        'assists': 0,
        'CS': 0,
        'gold': 0,
        'damage': 0,
        'tanking': 0
    }

    for player_num in range(1, 6):
        stats['kills'] += df[f'{prefix}_player{player_num}_K'].sum()
        stats['deaths'] += df[f'{prefix}_player{player_num}_D'].sum()
        stats['assists'] += df[f'{prefix}_player{player_num}_A'].sum()
        stats['CS'] += df[f'{prefix}_player{player_num}_CS'].sum()
        stats['gold'] += df[f'{prefix}_player{player_num}_gold'].sum()
        stats['damage'] += df[f'{prefix}_player{player_num}_damage'].sum()
        stats['tanking'] += df[f'{prefix}_player{player_num}_tanking'].sum()

    return stats


def process_team_data(input_file, output_file):
    """
    处理战队数据并生成汇总报告
    """
    # 读取CSV文件
    df = pd.read_csv(input_file)

    # 转换Duration为分钟（保留一位小数）
    df['Minutes'] = df['Duration'].apply(convert_duration_to_minutes)

    # 存储处理后的数据
    processed_data = []

    # 获取所有唯一的(matchType, team, region)组合
    unique_teams = set()

    # 从Team1和Team2中收集所有唯一的组合
    for team_num in [1, 2]:
        team_prefix = f'Team{team_num}'
        team_combinations = df.groupby(['matchType', team_prefix, f'{team_prefix}_region']).groups.keys()
        unique_teams.update(team_combinations)

    # 处理每个唯一的队伍组合
    for matchType, team, region in unique_teams:
        # 获取该队伍的所有比赛（作为Team1或Team2的比赛）
        team_matches_as_team1 = df[
            (df['matchType'] == matchType) &
            (df['Team1'] == team) &
            (df['Team1_region'] == region)
            ]

        team_matches_as_team2 = df[
            (df['matchType'] == matchType) &
            (df['Team2'] == team) &
            (df['Team2_region'] == region)
            ]

        # 计算统计数据
        stats_team1 = calculate_team_stats(team_matches_as_team1, team, 1)
        stats_team2 = calculate_team_stats(team_matches_as_team2, team, 2)

        # 合并统计数据
        total_stats = {
            'kills': stats_team1['kills'] + stats_team2['kills'],
            'deaths': stats_team1['deaths'] + stats_team2['deaths'],
            'assists': stats_team1['assists'] + stats_team2['assists'],
            'CS': stats_team1['CS'] + stats_team2['CS'],
            'gold': stats_team1['gold'] + stats_team2['gold'],
            'damage': stats_team1['damage'] + stats_team2['damage'],
            'tanking': stats_team1['tanking'] + stats_team2['tanking']
        }

        # 计算总比赛数和胜场数
        total_matches = len(team_matches_as_team1) + len(team_matches_as_team2)
        total_wins = len(team_matches_as_team1[team_matches_as_team1['win'] == team]) + \
                     len(team_matches_as_team2[team_matches_as_team2['win'] == team])

        # 计算总时长
        total_minutes = round(team_matches_as_team1['Minutes'].sum() +
                              team_matches_as_team2['Minutes'].sum(), 1)

        # 计算资源数据
        total_baron = team_matches_as_team1['Team1_Baron'].sum() + \
                      team_matches_as_team2['Team2_Baron'].sum()
        total_dra = team_matches_as_team1['Team1_Dra'].sum() + \
                    team_matches_as_team2['Team2_Dra'].sum()
        total_turts = team_matches_as_team1['Team1_Turts'].sum() + \
                      team_matches_as_team2['Team2_Turts'].sum()

        # 汇总数据
        summary = {
            'team': team,
            'region': region,
            'matchType': matchType,
            'Baron': int(total_baron),
            'Dra': int(total_dra),
            'Turts': int(total_turts),
            'kills': int(total_stats['kills']),
            'deaths': int(total_stats['deaths']),
            'assists': int(total_stats['assists']),
            'CS': int(total_stats['CS']),
            'gold': round(total_stats['gold'], 1),
            'damage': round(total_stats['damage'], 1),
            'tanking': round(total_stats['tanking'], 1),
            'matches_played': total_matches,
            'matches_won': total_wins,
            'minutes_played': round(total_minutes, 1)
        }

        processed_data.append(summary)

    # 创建结果DataFrame
    result_df = pd.DataFrame(processed_data)

    # 确保列的顺序符合要求
    column_order = [
        'team', 'region', 'matchType', 'Baron', 'Dra', 'Turts',
        'kills', 'deaths', 'assists', 'CS', 'gold', 'damage',
        'tanking', 'matches_played', 'matches_won', 'minutes_played'
    ]
    result_df = result_df[column_order]

    # 保存结果
    result_df.to_csv(output_file, index=False, encoding='utf-8')


# 使用函数
process_team_data('ori.csv', '01_team_new.csv')