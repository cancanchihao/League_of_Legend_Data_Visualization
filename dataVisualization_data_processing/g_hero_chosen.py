import pandas as pd
from datetime import datetime
import numpy as np


def convert_duration_to_minutes(duration_str):
    """
    Convert duration string to minutes (with one decimal place)
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


def standardize_names(df):
    """
    Standardize both player names and hero names:
    - Remove leading/trailing spaces
    - Convert to title case
    - Ensure consistent formatting
    """
    # Standardize player names
    for team_num in [1, 2]:
        for player_num in range(1, 6):
            name_col = f'Team{team_num}_player{player_num}_name'
            pick_col = f'Team{team_num}_player{player_num}_pick'

            # Standardize player names (first letter capital, rest lowercase)
            df[name_col] = df[name_col].str.strip().str.title()

            # Standardize hero names
            df[pick_col] = df[pick_col].str.strip().str.title()

    return df


def process_player_hero_choices(input_file, output_file):
    """
    Process player hero selection data and generate report with unified player data
    """
    # Read and prepare the data
    df = pd.read_csv(input_file)
    df['MatchDate'] = pd.to_datetime(df['MatchDate'], format='%Y-%m-%d')
    df = standardize_names(df)
    df['Minutes'] = df['Duration'].apply(convert_duration_to_minutes)

    # Store processed data
    processed_data = []

    # Create a mapping to store all matches for each player
    player_matches = {}

    # First pass: Collect all matches for each player
    for team_num in [1, 2]:
        team_prefix = f'Team{team_num}'

        for player_num in range(1, 6):
            name_col = f'{team_prefix}_player{player_num}_name'
            pick_col = f'{team_prefix}_player{player_num}_pick'

            # Iterate through all rows
            for _, row in df.iterrows():
                player_name = row[name_col]
                team = row[team_prefix]
                region = row[f'{team_prefix}_region']
                match_type = row['matchType']

                # Create player key
                player_key = (player_name, team, region, match_type)

                if player_key not in player_matches:
                    player_matches[player_key] = []

                # Store match data
                player_matches[player_key].append({
                    'date': row['MatchDate'],
                    'gameset': row['gameset'],
                    'hero': row[pick_col],
                    'won': row['win'] == team,
                    'minutes': row['Minutes']
                })

    # Second pass: Process collected data for each unique player
    for player_key, matches in player_matches.items():
        player_name, team, region, match_type = player_key

        # Sort matches by date and gameset
        sorted_matches = sorted(matches,
                                key=lambda x: (x['date'], x['gameset']),
                                reverse=True)

        # Get recent hero choices
        recent_picks = [match['hero'] for match in sorted_matches[:10]]

        # Pad with None if needed
        while len(recent_picks) < 10:
            recent_picks.append(None)

        # Calculate statistics
        player_stats = {
            'player_name': player_name,
            'player_team': team,
            'player_region': region,
            'matchType': match_type,
            'matches_played': len(matches),
            'minutes_played': round(sum(match['minutes'] for match in matches), 1),
            'matches_won': sum(1 for match in matches if match['won'])
        }

        # Add hero choices
        for i, hero in enumerate(recent_picks, 1):
            player_stats[f'hero_chosen_{i}'] = hero

        processed_data.append(player_stats)

    # Create and format result DataFrame
    result_df = pd.DataFrame(processed_data)

    # Ensure proper data types
    integer_columns = ['matches_played', 'matches_won']
    for col in integer_columns:
        result_df[col] = result_df[col].astype(int)

    result_df['minutes_played'] = result_df['minutes_played'].round(0).astype(int)

    # Sort columns
    first_cols = ['player_name', 'player_team', 'player_region', 'matchType',
                  'matches_played', 'minutes_played', 'matches_won']
    hero_cols = [f'hero_chosen_{i}' for i in range(1, 11)]
    result_df = result_df[first_cols + hero_cols]

    # Save result
    result_df.to_csv(output_file, index=False, encoding='utf-8')


# Use function
process_player_hero_choices('ori.csv', '07_hero_chosen_new.csv')