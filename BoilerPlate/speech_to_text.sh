#!/bin/bash

####
# file: speech_to_text.sh
# drafted by: Evan Upham; evan.upham@outlook.com;
# website: https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 3/31/2023
# revised: 3/31/2023
# reminder: chmod +x speech_to_text.sh
# reminder: ./speech_to_text.sh
# WARNING!!!: THIS IS UNTESTED
# 
# Creates Speech-to-Text folders. Rclone pulls files from OneDrive folder with WAV files to Input folder. 
# Pocketsphinx converts audio in the Input path to the text in the Output path.

# Check if Pocketsphinx and Pocketsphinx-en-us language model are installed
sudo apt-get install pocketsphinx pocketsphinx-en-us

# Set the project name and create the required folders
project_name="SpeechToText"
project_root="${HOME}/Pegboard/${project_name}"
mkdir -p "${project_root}"

# Set the Speech-to-Text root folder and its subfolders
stt_root="${project_root}/STT"
input_folder="${stt_root}/Input"
output_folder="${stt_root}/Output"

# Create the required subfolders if they do not exist
mkdir -p "${input_folder}"
mkdir -p "${output_folder}"

# Check if rclone is installed and configured for OneDrive
sudo apt-get install rclone

if ! rclone config show | grep -q 'onedrive'; then
  echo "rclone is not configured for OneDrive. Configuring..."
  rclone config
fi

# Refresh OneDrive folder
echo "Refreshing OneDrive folder..."
rclone sync "onedrive:/audio_input" "${input_folder}"

# Process all audio files in the input folder
for input_audio in "${input_folder}"/*.wav; do
  # Check if the input audio file exists
  if [ ! -f "${input_audio}" ]; then
    echo "No WAV files found in the input folder. Skipping the conversion process."
    break
  fi

  # Get the input audio filename without extension
  input_audio_base="$(basename "${input_audio}" .wav)"

  # Perform Speech-to-Text on the audio and save the recognized text to a text file
  output_file="${output_folder}/${input_audio_base}.txt"
  pocketsphinx_continuous -infile "${input_audio}" -logfn /dev/null > "${output_file}"

  echo "Processed ${input_audio} -> ${output_file}"
done

echo "Done."
