import pandas as pd
import numpy as np


def calculate_hero_wins(group, team_prefix, pick_col, hero_name):
    """
    计算英雄在特定分组中的胜场数

    Parameters:
    group - 数据分组
    team_prefix - 队伍前缀 (Team1 or Team2)
    pick_col - 英雄选择列名
    hero_name - 英雄名称

    Returns:
    int - 胜场数
    """
    win_condition = (group[team_prefix] == group['win']) & (group[pick_col] == hero_name)
    return win_condition.sum()


def process_hero_data(input_file, output_file):
    """
    处理英雄数据并生成统计报告
    """
    # 读取CSV文件
    df = pd.read_csv(input_file)

    # 存储处理后的数据
    processed_data = []

    # 获取所有赛段的比赛场次
    matches_per_type = df.groupby('matchType').size().to_dict()

    # 处理英雄选择数据
    for team_num in [1, 2]:
        team_prefix = f'Team{team_num}'

        # 处理每个位置的选择数据
        for player_num in range(1, 6):
            pick_col = f'{team_prefix}_player{player_num}_pick'

            # 标准化英雄名称
            df[pick_col] = df[pick_col].str.strip().str.title()

            # 按赛段和英雄分组统计
            picks_grouped = df.groupby(['matchType', pick_col])

            for (match_type, hero_name), group in picks_grouped:
                if pd.isna(hero_name) or hero_name == '':
                    continue

                # 统计该英雄在当前位置的数据
                position_map = {1: 'TOP', 2: 'JUG', 3: 'MID', 4: 'ADC', 5: 'SUP'}
                position = position_map[player_num]

                # 在处理picks的循环中：
                wins = calculate_hero_wins(group, team_prefix, pick_col, hero_name)

                summary = {
                    'hero_name': hero_name,
                    'position': position,
                    'matchType': match_type,
                    'pick_count': len(group),
                    'ban_count': 0,  # 禁用数据将在后面处理
                    'win_count': wins,
                    'matches_played': matches_per_type[match_type]
                }

                # 检查是否已存在相同的英雄-位置-赛段组合
                existing_entry = next(
                    (item for item in processed_data
                     if item['hero_name'] == hero_name
                     and item['position'] == position
                     and item['matchType'] == match_type),
                    None
                )

                if existing_entry:
                    # 更新现有条目
                    existing_entry['pick_count'] += summary['pick_count']
                    existing_entry['win_count'] += summary['win_count']
                else:
                    # 添加新条目
                    processed_data.append(summary)

    # 处理英雄禁用数据
    for team_num in [1, 2]:
        team_prefix = f'Team{team_num}'

        # 处理每个禁用位置
        for ban_num in range(1, 6):
            ban_col = f'{team_prefix}_ban{ban_num}'

            # 标准化英雄名称
            df[ban_col] = df[ban_col].str.strip().str.title()

            # 按赛段和英雄分组统计
            bans_grouped = df.groupby(['matchType', ban_col])

            for (match_type, hero_name), group in bans_grouped:
                if pd.isna(hero_name) or hero_name == '':
                    continue

                # 查找是否已存在该英雄的Ban记录
                existing_ban_entry = next(
                    (item for item in processed_data
                     if item['hero_name'] == hero_name
                     and item['position'] == 'Ban'
                     and item['matchType'] == match_type),
                    None
                )

                if existing_ban_entry:
                    # 更新现有Ban记录
                    existing_ban_entry['ban_count'] += len(group)
                else:
                    # 创建新的Ban记录
                    ban_summary = {
                        'hero_name': hero_name,
                        'position': 'Ban',
                        'matchType': match_type,
                        'pick_count': 0,
                        'ban_count': len(group),
                        'win_count': 0,
                        'matches_played': matches_per_type[match_type]
                    }
                    processed_data.append(ban_summary)

    # 创建结果DataFrame
    result_df = pd.DataFrame(processed_data)

    # 确保所有计数列为整数类型
    integer_columns = ['pick_count', 'ban_count', 'win_count', 'matches_played']
    for col in integer_columns:
        result_df[col] = result_df[col].astype(int)

    # 对结果进行排序
    result_df = result_df.sort_values(['matchType', 'hero_name', 'position'])

    # 保存结果
    result_df.to_csv(output_file, index=False, encoding='utf-8')


# 使用函数
process_hero_data('ori.csv', '03_hero_new.csv')