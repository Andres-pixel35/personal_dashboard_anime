import pandas as pd
from questionary import autocomplete
from config import blue_style, path_historical_csv, path_final_csv, final_csv, sort_final 
from manually import helpers

final_exists = helpers.final_exists(path_final_csv)
df = pd.read_csv(path_historical_csv)

if final_exists:
    final_df = pd.read_csv(path_final_csv)

choices = helpers.get_choices(df)

completer = helpers.fast_completer(choices)

is_in_final = False
is_in_session = False

new_entries = []

while True:
    answer = autocomplete(
        "Enter the title (or type 'exit' to finish): ",
        choices=[], 
        completer=completer,
        style=blue_style,
        qmark="💠",
    ).ask()

    # Break condition
    if not answer or answer.lower() == 'exit':
        break

    clean_title, clean_type = helpers.get_title_type(answer)
    if clean_title == 1 and clean_type == 1:
        print("ERROR: You need to choose the work you want to add, not just write it. Pleae try again.")
        continue

    # Check if it already exists in the main dataframe OR our current session list
    if final_exists:
        # Check if clean_title matches either 'title' OR 'english_title'
        mask = final_df["title"].eq(clean_title) | final_df["english_title"].eq(clean_title)
        is_in_final = bool(mask.any())

    is_in_session = any(
        ((row['title'] == clean_title) | (row['english_title'] == clean_title)).any()
        for row in new_entries
    )
 
    if is_in_final or is_in_session:
        print(f"'{clean_title}' is already in your list!")
        continue

    # Grab the data from the source dataframe
    match = df[
        ((df["title"] == clean_title) | (df["english_title"] == clean_title)) &
        (df["type"] == clean_type)
    ].copy()

    if not match.empty:
        # Calculate duration and add to our temporary session list
        match["complete_duration"] = match["duration"] * match["episodes"]
        new_entries.append(match)
        print(f"Added: {clean_title}")

# Batch add everything at once
if new_entries:
    to_concat = []
    
    
    if final_exists:
        to_concat.append(final_df)
    
    # Combine existing data (if any) with the new session entries
    final_df = pd.concat(to_concat + new_entries, ignore_index=True)

    final_df = helpers.sort_final(final_df, sort_final)

    try:
        final_df.to_csv(path_final_csv, index=False, encoding="utf-8")
        print("\n--- Summary ---")
        print(f"Success! {len(new_entries)} new rows saved to {final_csv}.")
    except Exception as e:
        print(f"Error saving {final_csv}: {e}")
        raise
else:
    print("No new changes to save.")
