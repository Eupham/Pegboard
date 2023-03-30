#!/bin/bash
set -euo pipefail

####
# file: log_terminal_sessions.sh
# drafted by: Evan Upham; evan.upham@outlook.com;
# https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 3/29/2023
# revised: 3/30/2023
# reminder: chmod +x log_terminal_sessions.sh
# This script sets up logging for terminal for a set directory


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