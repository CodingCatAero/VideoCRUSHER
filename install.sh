#!/bin/bash
set -eo pipefail

# Initializing this variable so bash is happy
packageSearch=""

# Determines what flavour of linux the user is running (Arch, Debiam, or Redhat)
# Then adjusts the package search and install commands accordingly
if [[ -f /etc/arch-release ]]; then
    echo "Arch-based OS detected"
    packageSearch="pacman -Q"
    packageInstall="sudo pacman -Syu"

elif [[ -f /etc/debian_version ]]; then
    echo "Debian-based OS detected"
    packageSearch="apt search"
    packageInstall="sudo aot-get install"

elif [[ -f /etc/redhat-release ]]; then
    echo "Redhat-based OS detected"
    packageSearch="rpm -qa | grep -w"
    packageInstall="dnf install"

else # If linux isn't found, program exits
    echo "Unsupported OS detected. Terminating"
    exit 1
fi

# If either dependency isn't installed, install it using the system's package manager
if ! $packageSearch python; then
    echo "Python not found. Installing..."
    $packageInstall python
fi

if ! $packageSearch ffmpeg; then
    echo "Ffmpeg not found. Installing..."
    $packageInstall ffmpeg
fi

# Adds or replaces the bash and python scripts for the user
sudo curl https://raw.githubusercontent.com/CodingCatAero/8mbDockerless/27c551c43d6b119853cb03f3a7cea3ec41751e32/8mb -o /usr/local/bin/8mb

sudo curl https://raw.githubusercontent.com/CodingCatAero/8mbDockerless/27c551c43d6b119853cb03f3a7cea3ec41751e32/8mb.py -o /usr/bin/8mb.py

sudo chmod +x /usr/local/bin/8mb

echo "Installed"