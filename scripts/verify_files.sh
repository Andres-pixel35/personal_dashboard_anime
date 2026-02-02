#!/bin/bash

# Pull all paths from Python into Bash variables in one go
eval $("$PY_BIN" -c "
    import config
    print(f'ORIGINAL_AIRING=\"{config.path_original_airing}\"')
    print(f'MODIFIED_AIRING=\"{config.path_modified_airing}\"')
    print(f'HISTORICAL_CSV=\"{config.path_historical_csv}\"')
")

# Put them in a list to iterate through the checks
files_paths=("$ORIGINAL_AIRING" "$MODIFIED_AIRING" "$HISTORICAL_CSV")

echo ""
echo "--- Starting verification of data files ---"

# iterates through all the array and make several verifications with each file
for path in ${files_paths[@]}; do
    filename="${path##*/}" # extract the filename
    mime_type=$(file -b --mime-type "$path") # checks the file type
  
    # checks whether the file exists or not and whether it has at least a size of 1 byte
    if [ ! -s "$path" ]; then
        echo ""
        echo "ERROR: File "$filename" does not exists at "$path", or it's empty."
        exit 2
    # checks wheter the file is csv or not
    elif [[ "$mime_type" != "text/csv" && "$filename" != *.csv ]]; then
        echo ""
        echo "ERROR: file "$filename" is not a csv file."
        exit 2
    fi
done

echo "All the file exists and are CSVs, you can proceed"
exit 0
