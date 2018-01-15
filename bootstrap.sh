#!/bin/bash

echo "Check if conda is installed..."
which -s conda

if [[ $? != 0 ]] ; then
    echo "Conda not found. Start conda installation..."
    if [ "$(uname)" == "Darwin" ]; then
        curl -O https://repo.continuum.io/archive/Anaconda3-4.3.0-MacOSX-x86_64.sh
        bash Anaconda3-4.3.0-MacOSX-x86_64.sh
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        wget https://repo.continuum.io/archive/Anaconda3-4.3.0-Linux-x86_64.sh
        bash Anaconda3-4.3.0-Linux-x86_64.sh
    fi

    #echo "export PATH=\"$HOME/anaconda3/bin:$PATH\"" >> ~/.bashrc
    source ~/.bashrc
else
    echo "conda already installed"
fi

echo "Installing requirements..."
conda install --yes --file requirements.txt

