#!/bin/bash


###WARNING I'M STILL TESTING THIS, AS IS, GOOD LUCK
####
# file: kaldi_setup.sh
# drafted by: Evan Upham; evan.upham@outlook.com;
# website: https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 3/31/2023
# revised: 4/1/2023
# reminder: chmod +x kaldi_setup.sh
# reminder: ./kaldi_setup.sh

# Import the arch4edu GPG key to your keyring
curl https://arch4edu.keybase.pub/arch4edu.gpg | gpg --import -

# Verify the key's fingerprint
gpg --fingerprint 7931B6D628C8D3BA

# Add the arch4edu repository to your pacman configuration file
echo "[arch4edu]" >> /etc/pacman.conf
echo "SigLevel = Required DatabaseOptional" >> /etc/pacman.conf
echo "Server = https://mirrors.tuna.tsinghua.edu.cn/arch4edu/\$arch" >> /etc/pacman.conf

# Refresh the package list to include the packages from the new repository
pacman -Sy

# Install the kaldi-openfst package from the arch4edu repository
pacman -S kaldi-openfst