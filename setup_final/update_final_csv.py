import pandas as pd
from config import path_modified_airing, path_final_csv, sort_final, final_csv 
from setup_final import helpers 

df_a = pd.read_csv(path_modified_airing)
df_f = pd.read_csv(path_final_csv)

for _, row in df_a.iterrows():
    # Match both Title AND Type at the same time
    mask = (df_f["title"] == row["title"]) & (df_f["type"] == row["type"])
    
    if mask.any():
        # Calculate complete duration
        row["complete_duration"] = row["duration"] * row["episodes"]
        
        # Update every row that matches both criteria
        df_f.loc[mask, :] = row.values

df_f = helpers.sort_final(df_f, sort_final)

try:
    df_f.to_csv(path_final_csv, index=False, encoding="utf-8")
    print(f"{final_csv} was successfully updated")
except Exception as e:
    print(f"Error updating {final_csv}: {e}")
    raise
