#!/bin/bash
set -euo pipefail

####
# file: log_terminal_sessions.sh
# drafted by: Evan Upham; evan.upham@outlook.com; https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 3/29/2023
# revised: 3/29/2023
# reminder: chmod +x log_terminal_sessions.sh
# This script sets up logging for terminal for a set directory and asks if you want to add to startup


echo "Do you want to add this script to startup? (y/n)"
read answer

if [ "$answer" == "y" ] || [ "$answer" == "Y" ]; then
    if ! grep -q "source ${HOME}/Pegboard/log_terminal_sessions.sh" "${HOME}/.bashrc"; then
        echo "source ${HOME}/Pegboard/log_terminal_sessions.sh" >> "${HOME}/.bashrc"
        echo "Script added to startup."
        
        # save a copy of bashrc to the log folder
        log_directory="$HOME/Pegboard/BubbleGum/log_folder"
        mkdir -p "$log_directory"
        cp "$I just finished getting my git repo set up.  I set the gitignore as well.  I have it ignoring 2 folders, *.json *.iso{HOME}/.bashrc" "${log_directory}/bashrc_$(date '+%Y-%m-%d_%H:%M:%S').txt"
        echo "bashrc file saved to the log folder."
    else
        echo "Script already added to startup."
        echo "Do you want to remove the script from startup? (y/n)"
        read remove_answer
        if [ "$remove_answer" == "y" ] || [ "$remove_answer" == "Y" ]; then
            sed -i '/source ${HOME}\/Pegboard\/log_terminal_sessions.sh/d' "${HOME}/.bashrc"
            echo "Script removed from startup."
        else
            echo "Script remains in startup."
        fi
    fi
else
    target_directories=(
        "${HOME}/Pegboard"
    )
    current_directory=$(pwd)

    if printf '%s\n' "${target_directories[@]}" | grep -q -F -x "$current_directory"; then
        log_directory="$HOME/Pegboard/BubbleGum/log_folder"
        mkdir -p "$log_directory"
        log_file="${log_directory}/$(date '+%Y-%m-%d').log"
        exec script -a -q -f "$log_file"
    fi
fi