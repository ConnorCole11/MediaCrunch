# MediaCrunch
A pyqt application for an increasingly lot of stuff.

## Purpose
To create an all-in-one GUI that is able to download songs and videos from youtube, and be able to play those songs offline instead of relying on youtube where I get easily distracted 🗿, and to easily edit those videos since the phone and computer for some reason can't do simple tasks like crop gifs 🗿.

Eventually, I want to be able to easily manipulate videos and stuff, to make them smaller size to be sendable on discord or in the rare case that making something low quality makes it funnier I want to be able to do that.

## Parts
The code has 4 main parts:
1. music_player
2. playlist_editor
3. yt_downloader
4. media_edit

---

### music_player

Just a music player. It's pretty cool

---
### playlist_editor

Basically lets you make a playlist using songs on your computer, and it creates a file that is readable by music_player so that you can always use that playlist in the future.

---
### yt_downloader

Downloads songs and videos from youtube with no issue, unless there's no permission to do so (rare). 

To download all of the videos in a playlist, use the playlist URL, select the "Enable Numbering" button, and enter "1" or whatever you want the first number to be. This will add something like "001_" "002_" to each filename to keep the songs in order in the folder. This just makes it easier to keep songs in the same order when you import a folder into the playlsit editor to make a playlist.

---

### media_edit

Not really implemented yet, but it'll edit videos and gifs and stuff. Bitrate, resolution, and other stuff that just makes the file way bigger even if the "improved quality" not noticeable.

# Setup

## Config

* First, open config.py (highly recommend using Visual Studio Code to work on any code.)
* Put in the path to the MediaCrunch folder (e.g. "/Applications/MediaCrunch/") for the 'mediaCrunch_path' variable.
* You can keep the rest of the stuff as a default. 

## Virtul Environment

1. Open the 'terminal' app
2. type `cd path/to/MediaCrunch` where 'path/to/MediaCrunch' is the path to the app's folder
3. type `python3 -m venv venvMedia`
4. You should see a folder called 'venvMedia'. That's a virtual environment, which will hold all of the packages the code uses. Now type `source venvMedia/bin/activate`
5. type `pip install -r requirements.txt` which automatically downloads all of the needed packages into the virtual environment.
6. (optional) Once that's done, you can type `deactivate` to get out of the vitual environment, since the next script will use it for you anyways. 

## Running the Code

* Type ./scripts/mac_run.sh to run the application on mac. Otherwise, in the root folder, do:

1. `source venvMedia/bin/activate`
2. `python -m src.main`

The code should run if set up properly.
