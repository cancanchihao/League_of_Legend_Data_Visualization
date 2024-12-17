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


def standardize_hero_names(df):
    """
    标准化所有英雄名称
    """
    for team_num in [1, 2]:
        for player_num in range(1, 6):
            col = f'Team{team_num}_player{player_num}_pick'
            df[col] = df[col].str.strip().str.title()
    return df


def get_hero_data(match_row, team_num, player_num):
    """
    获取单场比赛中特定英雄的数据
    """
    prefix = f'Team{team_num}_player{player_num}'
    return {
        'hero': match_row[f'{prefix}_pick'],
        'position': get_position(player_num),
        'kills': match_row[f'{prefix}_K'],
        'deaths': match_row[f'{prefix}_D'],
        'assists': match_row[f'{prefix}_A'],
        'CS': match_row[f'{prefix}_CS'],
        'gold': match_row[f'{prefix}_gold'],
        'damage': match_row[f'{prefix}_damage'],
        'tanking': match_row[f'{prefix}_tanking'],
        'team': match_row[f'Team{team_num}']
    }


def get_position(player_num):
    """
    将选手编号映射为位置名称
    """
    position_map = {1: 'TOP', 2: 'JUG', 3: 'MID', 4: 'ADC', 5: 'SUP'}
    return position_map[player_num]


def process_hero_vs_data(input_file, output_file):
    """
    处理英雄对位数据并生成统计报告
    """
    # 读取CSV文件
    df = pd.read_csv(input_file)
    df = standardize_hero_names(df)

    # 转换Duration为分钟
    df['Minutes'] = df['Duration'].apply(convert_duration_to_minutes)

    # 存储处理后的数据
    processed_data = []

    # 按赛段分组处理数据
    for match_type, match_type_group in df.groupby('matchType'):
        # 存储该赛段中的所有英雄对位数据
        hero_matchups = {}

        # 处理每场比赛
        for _, match in match_type_group.iterrows():
            # 收集Team1的英雄数据
            team1_heroes = []
            for p1 in range(1, 6):
                hero_data = get_hero_data(match, 1, p1)
                if not pd.isna(hero_data['hero']):
                    team1_heroes.append(hero_data)

            # 收集Team2的英雄数据
            team2_heroes = []
            for p2 in range(1, 6):
                hero_data = get_hero_data(match, 2, p2)
                if not pd.isna(hero_data['hero']):
                    team2_heroes.append(hero_data)

            # 处理所有可能的对位组合（5x5=25种组合）
            for hero1 in team1_heroes:
                for hero2 in team2_heroes:
                    # 使用tuple sorted确保对位组合的唯一性
                    matchup_key = tuple(sorted([
                        (hero1['hero'], hero1['position']),
                        (hero2['hero'], hero2['position'])
                    ]))

                    if matchup_key not in hero_matchups:
                        hero_matchups[matchup_key] = {
                            'hero1_name': matchup_key[0][0],
                            'hero1_position': matchup_key[0][1],
                            'hero2_name': matchup_key[1][0],
                            'hero2_position': matchup_key[1][1],
                            'matchType': match_type,
                            'matches_played': 0,
                            'minutes_played': 0,
                            'matches_won_1': 0,
                            'matches_won_2': 0,
                            'hero1_kills': 0, 'hero1_deaths': 0, 'hero1_assists': 0,
                            'hero1_CS': 0, 'hero1_gold': 0, 'hero1_damage': 0, 'hero1_tanking': 0,
                            'hero2_kills': 0, 'hero2_deaths': 0, 'hero2_assists': 0,
                            'hero2_CS': 0, 'hero2_gold': 0, 'hero2_damage': 0, 'hero2_tanking': 0
                        }

                    stats = hero_matchups[matchup_key]
                    stats['matches_played'] += 1
                    stats['minutes_played'] += match['Minutes']

                    # 更新胜场统计
                    if match['win'] == hero1['team']:
                        stats['matches_won_1'] += 1
                    if match['win'] == hero2['team']:
                        stats['matches_won_2'] += 1

                    # 更新英雄1的统计数据
                    stats['hero1_kills'] += hero1['kills']
                    stats['hero1_deaths'] += hero1['deaths']
                    stats['hero1_assists'] += hero1['assists']
                    stats['hero1_CS'] += hero1['CS']
                    stats['hero1_gold'] += hero1['gold']
                    stats['hero1_damage'] += hero1['damage']
                    stats['hero1_tanking'] += hero1['tanking']

                    # 更新英雄2的统计数据
                    stats['hero2_kills'] += hero2['kills']
                    stats['hero2_deaths'] += hero2['deaths']
                    stats['hero2_assists'] += hero2['assists']
                    stats['hero2_CS'] += hero2['CS']
                    stats['hero2_gold'] += hero2['gold']
                    stats['hero2_damage'] += hero2['damage']
                    stats['hero2_tanking'] += hero2['tanking']

        # 将所有对位数据添加到结果中
        processed_data.extend(hero_matchups.values())

    # 创建结果DataFrame
    result_df = pd.DataFrame(processed_data)

    # 处理数据精度
    float_columns = ['hero1_gold', 'hero1_damage', 'hero1_tanking',
                     'hero2_gold', 'hero2_damage', 'hero2_tanking']
    for col in float_columns:
        result_df[col] = result_df[col].round(1)

    # 确保整数列的类型
    int_columns = ['matches_played', 'minutes_played', 'matches_won_1', 'matches_won_2',
                   'hero1_kills', 'hero1_deaths', 'hero1_assists', 'hero1_CS',
                   'hero2_kills', 'hero2_deaths', 'hero2_assists', 'hero2_CS']
    for col in int_columns:
        result_df[col] = result_df[col].astype(int)

    # 保存结果
    result_df.to_csv(output_file, index=False, encoding='utf-8')


# 使用函数
process_hero_vs_data('ori.csv', '06_hero_vs_new.csv')