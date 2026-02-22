from questionary import Style

# -- user's name --
user_name = "Tricky"

# -- user's csv name --
user_csv = "works.csv"

# -- final csv name --
final_csv = "final.csv"

# -- change the way the program greets you --
greeting = "Good morning, User" # you need to set show_greetings to True to be able to see this message

# -- csv paths --
path_user_csv = "./data/user/" + user_csv
path_original_airing = "./data/original/airing_anime.csv"
path_modified_airing = "./data/modified/airing_anime_M.csv"
path_historical_csv = "./data/modified/anime.csv"
path_original_historical = "./data/original/anilist_seasonal_20251119.csv"
path_final_csv = "./data/final/" + final_csv

# -- Disable/Enable some features
# set to "True" if you want to skip the verification of the files every time you run the program (that they exists, they are csv files and that they have information)
disable_file_verification = False

# Set to True is you want to see "greeting" everytime you run the program
show_greetings = False

# Set either of them to True if you want to sort "final_csv", by default each entry will be in the order it was added.
# Take into account that if both of them are set to True, date takes priority and will be the only one applied
sort_final = {
    "date": True,
    "title": False
}

# set this to True if you care about having one piece with the episodes up to date, otherwise
# let it as false, since it will make updating_airing to take more time 
update_one_piece = True

# set this to False if you don't want to see the titles left unmatched at "sync your csv"
show_unmatched = True

# -- types filter --
valid_type = ["tv", "ona", "ova", "movie", "tv_short"] # these are the types the program will keep from airinga_anime.csv

# -- match name utility --
# if in your csv you tagged them with different names, here you can adapt them to you so they will match perfectly
# For example, instead of anime or tv you tagged them in your csv as "serie", then you just need to change either
# anime or tv for serie and they will be matched
type_mappings = {
    "anime": ["tv", "ova", "ona", "tv_short"],
    "tv": ["tv", "ova", "ona", "tv_short"],
    "movie": ["movie", "ona", "ova"],
    "film": ["movie", "ona", "ova"],
    "ona": ["tv", "movie", "ona", "tv_short"],
    "ova": ["tv", "ova", "movie"]
}

# -- Questionery looks configuration --
# here you can change the look of the thing that appears when you want to add a work or remove it.
blue_style = Style([
    ("qmark", "fg:#00d7ff bold"),       # The '?' icon
    ("question", "fg:#ffffff bold"),     # The actual question
    ("answer", "fg:#005fff bold"),       # The result after you press enter
    ("pointer", "fg:#00d7ff bold"),      # The arrow in lists
    ("highlighted", "fg:#00d7ff bold"),  # The currently hovered suggestion
    ("selected", "fg:#00afff"),          # The selected item
    ("text", "fg:#e4e4e4"),              # What you type
    # The dropdown menu colors
    ("completion-menu.completion", "bg:#000087 fg:#eeeeee"), 
    ("completion-menu.completion.current", "bg:#005fff fg:#ffffff"),
])

# -- some paths used exclusively for scripts/ --
# do not change anything here, unless the url changes. Should that happen, then check first the repository of this program.
# airing_anime.csv from LeoRiosaki's github
url = "https://raw.githubusercontent.com/LeoRigasaki/Anime-dataset/refs/heads/main/data/raw/airing_anime.csv" 
cleanup = "setup_final.cleanup_airing"
concatenate = "setup_final.concatenate"
