import pandas as pd
from setup_final import helpers
from config import path_original_airing, path_modified_airing, update_one_piece

df = pd.read_csv(path_original_airing, usecols=[2,3,6,7,8,10,11,15,16,18,31,36,52])

# the column "season" has values such as "WINTER 2025", i actually only care about the season and not the year in this column
# this function removes the year from the column
df = helpers.keep_season_only(df, "season")

if update_one_piece:
    df = helpers.update_one_piece(df)

df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
df = df.dropna(subset="start_date")

# this ensures that only airing anime form the past and current season are shown in the anime.csv dataser
df = helpers.filter_season(df)

# this ensures that only VALID_TYPES are shown, go to helpers.py to see which are those types
df = helpers.filter_type(df, "type")
# this ensures that if episodes is null, it will be fillin with next_episode
df = helpers.fill_episodes(df)
# this ensures that if season is null, it will be fillin with the season corresponding its month of release
df = helpers.fill_season(df)
# and remove the column we no longer need
df = df.drop("next_episode_number", axis=1)

df = df.sort_values(by="start_date")

try:
    df.to_csv(path_modified_airing, index=False, encoding="utf-8")
    print(f"\nairing_anime.csv succesfully saved at {path_modified_airing}.")
except Exception as e:
    print(f"\nError saving airing_anime.csv: {e}")
    raise
