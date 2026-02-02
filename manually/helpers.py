import pandas as pd
import re
from prompt_toolkit.completion import WordCompleter, ThreadedCompleter
from pathlib import Path

def fast_completer(choices_list):
    """
    Creates a threaded, space-aware completer for large lists.
    """
    # This regex pattern treats the entire input line as a single word,
    # which is what allows spaces to be searched correctly.
    everything_pattern = re.compile(r"^.*$")

    # We wrap the WordCompleter in a ThreadedCompleter so 
    # the UI doesn't lag
    return ThreadedCompleter(
        WordCompleter(
            choices_list,
            ignore_case=True,
            match_middle=True,
            pattern=everything_pattern
        )
    )

def get_choices(df):
    """
    get a df and return a list with all the native titles and english titles plus its type
    """ 
    choices = []
    for _, row in df.iterrows():
        t_type = f" ({row['type']})"
        
        # Add native title with type
        if pd.notna(row['title']):
            choices.append(f"{row['title']}{t_type}")
            
        # Add english title with type (if it exists)
        if pd.notna(row["english_title"]):
            choices.append(f"{row['english_title']}{t_type}")

    return choices

def get_title_type(answer):
    # Extract both parts from: "Adachi to Shimamura (tv)"
    try:
        clean_title = answer.rsplit(" (", 1)[0]
        clean_type = answer.rsplit(" (", 1)[1].rstrip(")")
    except Exception:
        return 1, 1

    return clean_title, clean_type

def sort_final(df, sort_final):
    if sort_final.get("date"):
        df = df.sort_values(by="start_date")
    elif sort_final.get("title"):
        df = df.sort_values(by="title", key=lambda col: col.str.lower())

    return df

def final_exists(filepath):
    """
    Checks if final exists and is not empty.
    Returns True if file exists and has content, False otherwise.
    """
    path = Path(filepath)

    if path.is_file() and path.stat().st_size > 0:
        return True
    
    return False




