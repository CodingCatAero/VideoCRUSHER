#!/bin/bash

if [[ ! -f /usr/local/bin/8mb ]]; then
    curl -s https://raw.githubusercontent.com/CodingCatAero/8mbDockerless/27c551c43d6b119853cb03f3a7cea3ec41751e32/8mb | sudo tee /usr/local/bin/8mb > /dev/null 
fi
    
if [[ ! -f /usr/local/bin/8mb.py ]]; then
    curl -s https://raw.githubusercontent.com/CodingCatAero/8mbDockerless/27c551c43d6b119853cb03f3a7cea3ec41751e32/8mb.py | sudo tee /usr/local/bin/8mb.py > /dev/null
fi

sudo chmod +x /usr/local/bin/8mb

echo "Installed"