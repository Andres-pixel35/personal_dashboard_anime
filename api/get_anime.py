from questionary import select
import pandas as pd
from config import valid_type, blue_style, path_historical_csv
from setup_final import helpers
from api import anilist

df1 = pd.read_csv(path_historical_csv)

choices = valid_type

title = input("Enter the title of the work you want to fetch: ")
work_type = select(
    "Select its type: ",
    choices=choices,
    style=blue_style,
    qmark="💠",
).ask()

if title.strip() and work_type:
    new_entry = anilist.fetch_anime_info(title, work_type)
    if len(new_entry) != 0:
        # first check that this anime does not exists already in anime.csv
        title_val = new_entry["title"].item()
        type_val = new_entry["type"].item()
        is_duplicate = ((df1["title"] == title_val) & (df1["type"] == type_val)).any()

        if not is_duplicate:
            # clean new entry
            new_entry = helpers.fill_episodes(new_entry)
            new_entry = new_entry.drop("next_episode_number", axis=1)
            new_entry = helpers.fill_season(new_entry)

            # concatenate both of them
            df = pd.concat([df1, new_entry.astype(df1.dtypes)], ignore_index=True)
            df.loc[:,"start_date"] = pd.to_datetime(df["start_date"]).dt.date
            df = df.sort_values(by="start_date")
            
            try:
                df.to_csv(path_historical_csv, index=False, encoding="utf-8")
                print(f"{title_val.title()} ({type_val.lower()}) was successfully added to anime.csv")
            except Exception as e:
                print(f"Error saving anime.csv: {e}")
                raise
        else:
            print(f"{title_val.title()} ({type_val.lower()}) already exists in anime.csv")
else:
    print("You either didn't enter a title or didn't select a type.")

