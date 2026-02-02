#!/bin/bash

echo "--- Activating virtual environment ---"

# if you prefer to use conda, add the following line changing conda for the model you are using
source ~/miniconda3/etc/profile.d/conda.sh

# also add this line with the actual name of your environment
conda activate maybe
# if you do the previous you should either remove or comment the following if statement


#if [ ! -z ".venv/" ]; then
#    source .venv/bin/activate
#else
#    echo "No virtual environment found, please create one and install the requirements."
#    echo "If you are using Conda, please add the necessary lines in main.sh"
#    exit 1
#fi

source ./scripts/helpers.sh

if [ -z "$PY_BIN" ]; then
    echo "ERROR: Python is required, but not found."
    deactivate
    exit 1
fi

# Exports variables from config.py
eval $("$PY_BIN" -c "
    import config
    print(f'GREETING=\"{config.greeting}\"')
    print(f'FINAL_CSV=\"{config.final_csv}\"')
    print(f'FINAL_PATH=\"{config.path_final_csv}\"')
    print(f'USER_CSV=\"{config.user_csv}\"')
    print(f'PATH_USER_CSV=\"{config.path_user_csv}\"')
    print(f'DISABLE_VERIFICATION={str(config.disable_file_verification).lower()}')
    print(f'SHOW_GREETINGS={str(config.show_greetings).lower()}')
")

if [ "$SHOW_GREETINGS" == "true" ]; then
    figlet -f slant -t -c "$GREETING" | lolcat
fi

if [ "$DISABLE_VERIFICATION" == "false" ]; then
    ./scripts/verify_files.sh "$PY_BIN"
    status=$?
    check_status "$status"
fi

OPTIONS=( "Sync your csv" "Add work" "Remove Work" "Dashboard" "Update Airing" "Update Final" "Fetch From Anilist" "Update anime" "Exit" )
len=${#OPTIONS[@]}

while true; do
    echo ""
    echo "What do you want to do?"

    for ((i=0; i<$len; i++)); do
        echo ""$((i+1))": "${OPTIONS[$i]}""
    done

    read -p "Please enter the number: " action

    case "$action" in
        1)
            if file_exists "$PATH_USER_CSV" "$USER_CSV"; then
                echo ""
                echo -n "This action will match "$USER_CSV" with anime.csv and it will create "$FINAL_CSV" with all" 
                echo " the matches and the complete information"
                if confirm "Do you want to proceed? " "Y"; then
                    echo "Creating "$FINAL_CSV" please wait a moment..."
                    "$PY_BIN" -m setup_final.match_name

                    status=$?
                    check_status "$status"

                    ask_continue && continue || break
                else
                    echo "Going back to actions."
                    continue
                fi
            else
                ask_continue && continue || break
            fi
        ;;
        2)
            echo ""
            "$PY_BIN" -m manually.add_work
            
            status=$?
            check_status "$status"

            ask_continue && continue || break
        ;;
        3)
            echo ""
            if file_exists "$FINAL_PATH" "$FINAL_CSV"; then 
                "$PY_BIN" -m manually.remove_work

                status=$?
                check_status "$status"

                ask_continue && continue || break
            else
                ask_continue && continue || break
            fi
        ;;
        4)
            echo ""
            file_exists "$FINAL_PATH" "$FINAL_CSV" && {
                echo "To stop the app press \"ctrl + c\""
                "$PY_BIN" -m streamlit run ./dashboard/dashboard.py              
            }
 
            ask_continue && continue || break
        ;;
        5) 
            echo ""
            echo -n "This action will download airing_anime.csv from LeoRiosaki's github, then it will clean that file and "
            echo "concatenate it with anime.csv"

            if confirm "Do you want to proceed?" "Y"; then
                ./scripts/update.sh "$PY_BIN"

                status=$?
                check_status "$status"

                ask_continue && continue || break
            else
                echo "Going back to actions."
                continue
            fi
        ;;
        6)
            echo ""
            if file_exists "$FINAL_PATH" "$FINAL_CSV"; then
                echo "This action will update the airing works in "$FINAL_CSV" with the information from airing_anime_M.csv"

                if confirm "Do you want to proceed?" "Y"; then
                    "$PY_BIN" -m setup_final.update_final_csv

                    status=$?
                    check_status "$status"

                    ask_continue && continue || break
                else
                    echo "Going back to actions."
                    continue
                fi
            else
                ask_continue && continue || break
            fi
        ;;
        7)
            echo ""
            "$PY_BIN" -m api.get_anime

            status=$?
            check_status "$status"

            ask_continue && continue || break
        ;;
        8)
            echo ""
            echo "This action will replace anime.csv from data/modified, if exists, cleaning the original csv"

            if confirm "Do you want to proceed?" "Y"; then
                "$PY_BIN" -m setup_final.cleanup_historical && "$PY_BIN" -m setup_final.fillna

                status=$?
                check_status "$status"

                ask_continue && continue || break
            else
                echo "Going back to actions."
                continue
            fi
        ;;
        9)
            break
        ;;
        *)
            echo ""
            echo "You need to choose a number between 1 and "$len", please try again."
        ;;
    esac
done
        
echo ""
echo "-- Closing virtual environment ---"

# conda deactivate 
conda deactivate # remove or commment this line if you are using conda and add the previous one 

exit 0
