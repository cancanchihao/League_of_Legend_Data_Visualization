import pandas as pd
from datetime import datetime
import numpy as np
from itertools import combinations


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


def get_player_position(player_num):
    """
    将选手编号映射为位置名称
    """
    position_map = {1: 'TOP', 2: 'JUG', 3: 'MID', 4: 'ADC', 5: 'SUP'}
    return position_map[player_num]


def standardize_player_names(df):
    """
    标准化所有选手名称
    """
    for team_num in [1, 2]:
        for player_num in range(1, 6):
            col = f'Team{team_num}_player{player_num}_name'
            df[col] = df[col].str.strip().str.title()
    return df


def process_team_matchups(input_file, output_file):
    """
    处理队伍对位数据并生成统计报告
    """
    # 读取CSV文件
    df = pd.read_csv(input_file)

    # 标准化选手名称
    df = standardize_player_names(df)

    # 转换Duration为分钟
    df['Minutes'] = df['Duration'].apply(convert_duration_to_minutes)

    # 存储处理后的数据
    processed_data = []

    # 按赛段分组处理数据
    for match_type, match_type_group in df.groupby('matchType'):
        # 获取该赛段中所有唯一的队伍组合
        unique_teams = set()
        for _, row in match_type_group.iterrows():
            # 确保队伍对的顺序一致（字母序）
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

            # 初始化数据结构
            matchup_data = {
                'Team1_name': team1,
                'Team1_region': region1,
                'Team2_name': team2,
                'Team2_region': region2,
                'matchType': match_type,
                'matches_played': len(team_matches),
                'minutes_played': round(team_matches['Minutes'].sum(), 1)
            }

            # 处理每个队伍的选手数据
            for team_idx, (team, region) in enumerate([(team1, region1), (team2, region2)], 1):
                team_prefix = f'Team{team_idx}'

                for player_num in range(1, 6):
                    # 获取该选手在所有比赛中的数据
                    total_stats = {
                        'kills': 0,
                        'deaths': 0,
                        'assists': 0,
                        'CS': 0,
                        'gold': 0,
                        'damage': 0,
                        'tanking': 0
                    }

                    position = get_player_position(player_num)
                    player_name = None

                    # 分别处理作为Team1和Team2时的数据
                    for orig_team_num in [1, 2]:
                        mask = team_matches[f'Team{orig_team_num}'] == team
                        if not mask.any():
                            continue

                        filtered_matches = team_matches[mask]
                        if player_name is None:
                            player_name = filtered_matches[f'Team{orig_team_num}_player{player_num}_name'].iloc[0]

                        # 累加统计数据
                        for stat, stat_suffix in [
                            ('kills', '_K'),
                            ('deaths', '_D'),
                            ('assists', '_A'),
                            ('CS', '_CS'),
                            ('gold', '_gold'),
                            ('damage', '_damage'),
                            ('tanking', '_tanking')
                        ]:
                            col = f'Team{orig_team_num}_player{player_num}{stat_suffix}'
                            total_stats[stat] += filtered_matches[col].sum()

                    # 添加该选手的数据到matchup_data
                    matchup_data.update({
                        f'{team_prefix}_player{player_num}_name': player_name,
                        f'{team_prefix}_player{player_num}_position': position,
                        f'{team_prefix}_player{player_num}_kills': int(total_stats['kills']),
                        f'{team_prefix}_player{player_num}_deaths': int(total_stats['deaths']),
                        f'{team_prefix}_player{player_num}_assists': int(total_stats['assists']),
                        f'{team_prefix}_player{player_num}_CS': int(total_stats['CS']),
                        f'{team_prefix}_player{player_num}_gold': round(total_stats['gold'], 1),
                        f'{team_prefix}_player{player_num}_damage': round(total_stats['damage'], 1),
                        f'{team_prefix}_player{player_num}_tanking': round(total_stats['tanking'], 1)
                    })

            processed_data.append(matchup_data)

    # 创建结果DataFrame
    result_df = pd.DataFrame(processed_data)

    # 保存结果
    result_df.to_csv(output_file, index=False, encoding='utf-8')


# 使用函数
process_team_matchups('ori.csv', '05_player_vs_new.csv')