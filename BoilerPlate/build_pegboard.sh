#!/bin/bash
set -euo pipefail

####
# file: build_pegboard.sh
# drafted by: Evan Upham; evan.upham@outlook.com; https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 3/29/2023
# revised: 4/1/2023
# reminder: chmod +x build_pegboard.sh
# warning: This script ran successfully after a revision
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

if [ -d "${pegboard_dir}/.git" ]; then
    echo "Pegboard repo already cloned."
    cd "${pegboard_dir}"
else
    # Prompt user for git username and email
    read -rp "Enter git username: " git_username
    read -rp "Enter git email: " git_email

    # Set git username and email globally
    git config --global user.name "$git_username"
    git config --global user.email "$git_email"

    # Clone git repo
    git clone https://github.com/Eupham/Pegboard.git "${pegboard_dir}"

    # Navigate to the cloned repository
    cd "${pegboard_dir}"
fi

# Fetch the changes from the remote repository
git fetch origin

# Reset the local branch to be in sync with the remote main branch
git reset --hard origin/main

# Create virtual environment if not exists
if [ ! -d "${pegboard_dir}/BubbleGum" ]; then
    python -m venv "${pegboard_dir}/BubbleGum"
fi

# Activate virtual environment
source "${pegboard_dir}/BubbleGum/bin/activate"

# Deactivate virtual environment
deactivate

# Create Pegboard directory and subdirectories
mkdir -p "${boilerplate_dir}" "${ducttape_dir}"

# Navigate back to the initial directory
cd -

echo "Pegboard repo cloned and synced successfully."