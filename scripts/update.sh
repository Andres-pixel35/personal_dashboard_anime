#!/bin/bash

# Capture Python variables into Bash environment
eval $("$PY_BIN" -c "
    import config
    print(f'URL=\"{config.url}\"')
    print(f'CLEANUP_SCRIPT=\"{config.cleanup}\"')
    print(f'CONCAT_SCRIPT=\"{config.concatenate}\"')
    print(f'SAVE_AIRING=\"{config.path_original_airing}\"')
")

# download the new airing_anime.csv
echo ""
echo "Downloading airing_anime.csv from Github"
echo "--------------------------------"
if ! curl -f -L -o "$SAVE_AIRING" "$URL"; then
    echo "Download of airing_anime.csv from GitHub failed"
    exit 1
fi

# cleans that new file and concatenate it with anime.csv
echo ""
echo "Cleaning and concatenating airing file with anime.csv"
echo "--------------------------------"
"$1" -m "$CLEANUP_SCRIPT" && "$1" -m "$CONCAT_SCRIPT"

exit 0




