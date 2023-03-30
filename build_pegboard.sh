#!/bin/bash
set -euo pipefail

####
# file: build_pegboard.sh
# drafted by: Evan Upham; evan.upham@outlook.com; https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 3/29/2023
# revised: 3/29/2023
# reminder: chmod +x build_pegboard.sh
# warning: This script hasn't been tested on a blank slate yet.
# This script sets up a Pegboard env for drafting and pulls.

pegboard_dir="${HOME}/Pegboard"
boilerplate_dir="${pegboard_dir}/BoilerPlate"
ducttape_dir="${pegboard_dir}/Ducttape"

# Check if Python and Git are installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed."
    exit 1
fi

# Create Pegboard directory and subdirectories
mkdir -p "${boilerplate_dir}" "${ducttape_dir}"

if [ -d "${pegboard_dir}/Pegboard" ]; then
    echo "Pegboard repo already cloned."
else
    # Prompt user for git username and email
    read -rp "Enter git username: " git_username
    read -rp "Enter git email: " git_email

    # Set git username and email globally
    git config --global user.name "$git_username"
    git config --global user.email "$git_email"

    # Create virtual environment
    python -m venv "${pegboard_dir}/BubbleGum"

    # Activate virtual environment
    source "${pegboard_dir}/BubbleGum/bin/activate"

    # Deactivate virtual environment
    deactivate

    # Clone git repo
    git clone https://github.com/Eupham/Pegboard.git "${pegboard_dir}/Pegboard"

    echo "Pegboard repo cloned successfully."
fi