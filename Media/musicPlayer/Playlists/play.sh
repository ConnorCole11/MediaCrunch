#!/bin/bash

# Exit if no argument is provided
if [ -z "$1" ]; then
    echo "Usage: ./play.sh <playlist_file>"
    exit 1
fi

# Activate virtual environment
source ~/Desktop/Media/venv_media/bin/activate

# Run Python script with the provided playlist argument
python ../main.py --Playlist "$1"
