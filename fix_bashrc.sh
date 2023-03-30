#!/bin/bash
set -euo pipefail

####
# file: fix_bashrc.sh
# drafted by:Evan Upham; evan.upham@outlook.com; https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 3/30/2023
# revised: 3/30/2023
# reminder: chmod +x fix_bashrc.sh
# This script fixes issues with .bashrc by rolling it back



# Define the path to the .bashrc file
bashrc_path="$HOME/.bashrc"

# Create a backup of the current .bashrc file
cp "$bashrc_path" "${bashrc_path}.bak"

# Restore the default .bashrc file from the /etc/skel/ directory
cp /etc/skel/.bashrc "$bashrc_path"

# Print a message indicating that the script has finished running
echo "The .bashrc file has been restored to its default state."