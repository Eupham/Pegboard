#!/bin/bash
set -euo pipefail

# Remove the existing React Native project directory
rm -rf HelloWorld

# Reinstall the React Native CLI
npm uninstall -g react-native-cli
npm install -g react-native-cli

# Create a new React Native project
react-native init HelloWorld

# Change into the project directory
cd HelloWorld

# Install the required dependencies
npm install

# Build and run the project on an Android emulator or connected device
react-native run-android

# Open the project in Visual Studio Code
code .
