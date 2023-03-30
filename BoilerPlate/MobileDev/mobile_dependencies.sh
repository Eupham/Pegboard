#!/bin/bash
set -euo pipefail

####
# file: mobile_dependencies.sh
# drafted by: Evan Upham; evan.upham@outlook.com; https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 3/30/2023
# revised: 3/30/2023
# reminder: chmod +x mobile_dependencies.sh
# warning: This script hasn't been tested yet
# This script sets up mobile dev dependencies


# Install Git
sudo pacman -S git code nodejs npm

# Install react-native-cli
sudo npm install -g react-native-cli

# Install Android SDK
sudo pacman -S gradle