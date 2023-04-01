#!/bin/bash

####
# file: tesserect_io_folders.sh
# drafted by:Evan Upham; evan.upham@outlook.com; https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 3/31/2023
# revised: 3/31/2023
# reminder: chmod +x tesserect_io_folders.sh
# Creates Tesseract folders.  Rclone pulls files from onedrive folder with pngs to input folder.  Tesserect converts images in the input path to the text in the output path
#!/bin/bash

# Check if Tesseract, Tesseract data are installed
sudo pacman -S  --needed tesseract tesseract-data-eng


# Set the project name and create the required folders
project_name="TesserectPng2Txt"
project_root="${HOME}/Pegboard/${project_name}"
mkdir -p "${project_root}"

# Set the OCR root folder and its subfolders
ocr_root="${project_root}/OCR"
input_folder="${ocr_root}/Input"
output_folder="${ocr_root}/Output"

# Create the required subfolders if they do not exist
mkdir -p "${input_folder}"
mkdir -p "${output_folder}"

# Check if rclone is installed and configured for OneDrive
sudo pacman -S --needed rclone

if ! rclone config show | grep -q 'onedrive'; then
  echo "rclone is not configured for OneDrive. Configuring..."
  rclone config
fi

# Refresh OneDrive folder
echo "Refreshing OneDrive folder..."
rclone sync "onedrive:/OCR_INPUT" "${input_folder}"

# Process all PNG images in the input folder
for input_image in "${input_folder}"/*.png; do
  # Check if the input image file exists
  if [ ! -f "${input_image}" ]; then
    echo "No PNG images found in the input folder. Skipping the conversion process."
    break
  fi

  # Get the input image filename without extension
  input_image_base="$(basename "${input_image}" .png)"

  # Perform OCR on the PNG image and save the recognized text to a text file
  output_file="${output_folder}/${input_image_base}.txt"
  tesseract "${input_image}" "${output_file}"

  echo "Processed ${input_image} -> ${output_file}"
done

echo "Done."