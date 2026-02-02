import pandas as pd
from pathlib import Path
from questionary import autocomplete, confirm
from config import blue_style, path_final_csv, final_csv
from manually import helpers

df = pd.read_csv(path_final_csv)

choices = helpers.get_choices(df)

completer = helpers.fast_completer(choices)

# List to keep track of indices we intend to remove
indices_to_drop = []
# List of titles (for visual confirmation at the end)
removed_titles = []

while True:
    answer = autocomplete(
        "Enter the title you want to remove (or type 'exit' to finish): ",
        choices=choices,
        completer=completer,
        style=blue_style,
        qmark="💠", 
    ).ask()

    if not answer or answer.lower() == 'exit':
        break

    clean_title, clean_type = helpers.get_title_type(answer)
    if clean_title == 1 and clean_type == 1:
        print("ERROR: You need to choose the work you want to remove, not just write it. Pleae try again.")
        continue

    # Find the rows that match the criteria
    matching_rows = df[
        ((df["title"] == clean_title) | (df["english_title"] == clean_title)) &
        (df["type"] == clean_type)
    ]

    # Ask for confirmation
    is_confirmed = confirm(
        f"Are you sure you want to remove {clean_title} ({clean_type.lower()})?",
        default=False
    ).ask()

    if is_confirmed:
        indices_to_drop.extend(matching_rows.index.tolist())
        removed_titles.append(f"{clean_title} ({clean_type})")
        print(f"Marked '{clean_title}' for removal.")
    else:
        print("Deletion canceled.")

# Finalize: Drop all marked rows at once
if indices_to_drop:
    # We use list(set()) to ensure we don't try to drop the same index twice
    df = df.drop(index=list(set(indices_to_drop)))
    
    

    # removes file if there is no information to avoid errors with dashboard and remoce_work itself in the future
    if len(df) == 0:
        Path.unlink(path_final_csv)
        print(f"\nSince you deleted all the information from {final_csv}, that file was also removed.")
    else: 
        try:
            df.to_csv(path_final_csv, index=False, encoding="utf-8")
            print("\n--- Summary ---")
            print(f"Successfully removed {len(removed_titles)} items:")
            for title in removed_titles:
                print(f" - {title}")
        except Exception as e:
            print(f"Error saving {final_csv}: {e}")
            raise
else:
    print("No items were removed.")
