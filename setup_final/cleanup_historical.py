import pandas as pd
from setup_final import helpers
from config import path_original_historical, path_historical_csv

df = pd.read_csv(path_original_historical, usecols=[2,3,6,7,8,10,11,15,16,18,31,36])
df = helpers.keep_season_only(df, "season")
df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
df = df.dropna(subset="start_date")
df = helpers.filter_type(df, "type")

try:
    df.to_csv(path_historical_csv, index=False, encoding="utf-8")
    print(f"anime.csv was successfully created at {path_historical_csv}")
except Exception as e:
    print(f"Error creating anime.csv {e}")
    raise
