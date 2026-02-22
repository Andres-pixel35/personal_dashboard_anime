from datetime import datetime
import pandas as pd
from config import valid_type
from api import anilist
import numpy as np

SEASONS = ["winter", "spring", "summer", "fall"]

def keep_season_only(df, column_name):
    # Split the string in column_name and only the first string is keep.

    df[column_name] = df[column_name].str.split().str[0]
    return df

# if the current month is bigger than 10, then we are in the last season of the year and i don't care about shutting out any anime
# from this year, only about the next year.
# In the opposite case, depending of the month I shutout the yet to come season.
# as you can see in the first inner if, if we are in the first season then it shutout spring, summer and fall
def filter_season(df):
    now = datetime.now()
    current_month, current_year = now.month, now.year

    if current_month < 10:

        if current_month >= 1 and current_month < 4:
            del SEASONS[0]
        elif current_month >= 4 and current_month < 7:
            del SEASONS[0:2]
        elif current_month >= 7 and current_month < 10:
            del SEASONS[0:3]

        df = df[~((df["season"].str.lower().isin(SEASONS) & (df["start_date"].dt.year == current_year)))]
    else:
        df = df[~(df["start_date"].dt.year == current_year + 1)]

    return df
    

def filter_type(df, column_name):
    df = df[df[column_name].str.lower().isin(valid_type)]
    return df

def sort_final(df, sort_final):
    if sort_final.get("date"):
        df = df.sort_values(by="start_date")
    elif sort_final.get("title"):
        df = df.sort_values(by="title", key=lambda col: col.str.lower())

    return df

def fill_episodes(df):
    """
    fill the null values in the column "episodes" using "next_episode_number" 
    """

    df = df.copy()
    # Ensure columns are numeric (floats)
    df["episodes"] = pd.to_numeric(df["episodes"], errors='coerce')
    df["next_episode_number"] = pd.to_numeric(df["next_episode_number"], errors='coerce')
    
    # Calculate what the "filled" values SHOULD be
    # This creates a temporary series where next_ep 1 becomes 1, and 5 becomes 4
    calculated_fills = (df["next_episode_number"] - 1).clip(lower=1)
    
    # Fill only the missing values in "episodes" using the calculation
    df["episodes"] = df["episodes"].fillna(calculated_fills)
    
    return df

def fill_season(df):
    """
    fill the null values in the column "season" using the month from "start_date"
    """

    df = df.copy()
    df["start_date"] = pd.to_datetime(df["start_date"])
    
    # Extract months for the whole column at once
    month = df["start_date"].dt.month

    # Create masks for the conditions
    winter = (month < 4)
    spring = (month >= 4) & (month < 7)
    summer = (month >= 7) & (month < 10)
    fall = (month >= 10)

    # Only fill where "season" is currently null
    is_null = df["season"].isna()

    df.loc[is_null & winter, "season"] = "WINTER"
    df.loc[is_null & spring, "season"] = "SPRING"
    df.loc[is_null & summer, "season"] = "SUMMER"
    df.loc[is_null & fall, "season"] = "FALL"

    return df

def update_one_piece(df):
    print("Updatin One Piece (if you don't want this disable it in config.py)")
    one_piece = anilist.fetch_anime_info("one piece", "tv")

    df_final = pd.concat([df, one_piece.astype(df.dtypes)], ignore_index=True)

    return df_final

def show_unmatched(titles: list): 
    if titles:
        print("\n--- Unmatched Anime ---")
        for title in titles: 
            print(f"- {title}")
    else:
        print("All your Anime were successfully matched")

# Takes a df and a column and return the index of the rows
def index_null_values(df, columns: list):
    index_list = []

    for column in columns:

        mask = df[column].isnull() 

        index = df[mask].index

        index_list.append(index)

    return index_list 

def fill_na_values(df, index: list, columns: list, values: list):
    for i in range(len(columns)):
        col = columns[i]
        idx = index[i]
        val = values[i]
        
        # Check if we are dealing with the score column
        if col == 'score':
            size = len(idx)
            if size > 0:
                # We assume 'val' is the distribution of existing scores
                samples = np.random.choice(val, size=size)
                df.loc[idx, col] = samples
        else:
            # For other columns, 'val' is a static value (1, "OTHER", etc.)
            df.loc[idx, col] = val
            
    return df

