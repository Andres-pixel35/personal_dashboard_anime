import pandas as pd
from setup_final import helpers
from config import path_historical_csv

df = pd.read_csv(path_historical_csv)

movie = df[df["type"].str.lower() == "movie"]
ona = df[df["type"].str.lower() == "ona"]
ova = df[df["type"].str.lower() == "ova"]
tv = df[df["type"].str.lower() == "tv"]
tv_short = df[df["type"].str.lower() == "tv_short"]


# columns that will be fill in all the types
COLUMNS = ["episodes", "duration", "source", "score"]

# -- MOVIE --

index = helpers.index_null_values(movie, COLUMNS)

median_duration = movie["duration"].median()
mean_score = round(movie["score"].mean(), 0)

df = helpers.fill_na_values(df, index, COLUMNS, [1, median_duration, "OTHER", mean_score])

# -- ONA --

index = helpers.index_null_values(ona, COLUMNS)

median_episodes = ona["episodes"].median()
median_duration = ona["duration"].median()
mean_score = round(ona["score"].mean(), 0)

df = helpers.fill_na_values(df, index, COLUMNS, [median_episodes, median_duration, "OTHER", mean_score])

# -- OVA --

index = helpers.index_null_values(ova, COLUMNS)

median_episodes = ova["episodes"].median()
median_duration = ova["duration"].median()
mean_score = round(ova["score"].mean(), 0)

df = helpers.fill_na_values(df, index, COLUMNS, [median_episodes, median_duration, "OTHER", mean_score])

# -- TV --

index = helpers.index_null_values(tv, COLUMNS)

median_episodes = tv["episodes"].median()
median_duration = tv["duration"].median()
mean_score = round(tv["score"].median(), 0)

df = helpers.fill_na_values(df, index, COLUMNS, [median_episodes, median_duration, "OTHER", mean_score])

# -- TV_SHORT --
index = helpers.index_null_values(tv_short, COLUMNS)

median_episodes = tv_short["episodes"].median()
median_duration = tv_short["duration"].median()
mean_score = round(tv_short["score"].median(), 0)

df = helpers.fill_na_values(df, index, COLUMNS, [median_episodes, median_duration, "OTHER", mean_score])

try:
    df.to_csv(path_historical_csv, index=False, encoding="utf-8")
    print(f"anime.csv was successfully fillin at {path_historical_csv}")
except Exception as e:
    print(f"Error filling in anime.csv: {e}")
    raise

