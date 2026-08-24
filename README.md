# MediaCrunch

A PyQt-based all-in-one media application for downloading, organizing, playing, and editing media.

## Purpose

MediaCrunch is designed to provide a single GUI for a variety of common media tasks.

Its current functionality includes:

- Downloading songs and videos from YouTube
- Playing downloaded music offline
- Creating and managing playlists
- Organizing locally stored music
- Basic video editing functionality

The long-term goal is to make it easy to manipulate and optimize videos and GIFs without needing several different applications. This includes tasks such as cropping GIFs, changing video resolution and bitrate, and reducing file sizes for services with file-size limits such as Discord.

---

# Setup

## Requirements

- Python 3.13
- FFmpeg
- macOS or Windows
- Visual Studio Code is recommended for working with the source code

## Configuration

Before running MediaCrunch, open `config.py`.

Set the `mediaCrunch_path` variable to the path of the MediaCrunch folder.

For example, on macOS:

    mediaCrunch_path = "/Applications/MediaCrunch/"

On Windows, use the path to the MediaCrunch folder on your system.

The remaining configuration options can generally be left at their default values.

---

## Virtual Environment

MediaCrunch uses a Python virtual environment to keep its dependencies isolated from other Python projects on the computer.

### macOS

1. Open Terminal.

2. Navigate to the MediaCrunch folder:

       cd path/to/MediaCrunch

3. Create the virtual environment:

       python3 -m venv venvMedia

4. Activate the virtual environment:

       source venvMedia/bin/activate

5. Install the required packages:

       pip install -r requirements.txt

The `venvMedia` folder now contains the Python environment and packages used by MediaCrunch.

Once setup is complete, the virtual environment can optionally be deactivated:

       deactivate

The provided run script will activate the environment automatically.

### Windows

1. Open PowerShell.

2. Navigate to the MediaCrunch folder:

       cd path\to\MediaCrunch

3. Create the virtual environment:

       python -m venv venvMedia

4. Activate the virtual environment:

       .\venvMedia\Scripts\Activate.ps1

5. Install the required packages:

       python -m pip install -r requirements.txt

If PowerShell prevents the activation script from running, the execution policy may need to be changed for the current user:

       Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

---

# Running MediaCrunch

## macOS

The easiest way to run MediaCrunch on macOS is to use the provided run script.

From the root MediaCrunch folder:

    ./scripts/mac_run.sh

Alternatively, the application can be started manually:

    source venvMedia/bin/activate
    python -m src.main

## Windows

From the root MediaCrunch folder:

    .\scripts\win_run.ps1

Alternatively, the application can be started manually:

    .\venvMedia\Scripts\Activate.ps1
    python -m src.main

If everything has been configured correctly, the MediaCrunch GUI should launch.

---

# Project Structure

    MediaCrunch/
    ├── README.md
    ├── config.py
    ├── requirements.txt
    ├── scripts/
    │   ├── mac_run.sh
    │   ├── mac_setup.sh
    │   ├── win_run.ps1
    │   └── win_setup.ps1
    └── src/
        ├── cookies.txt
        ├── main.py
        ├── master_gui.py
        │
        ├── media_edit/
        │   ├── audio_edit/
        │   └── video_edit/
        │       ├── gui/
        │       │   ├── config_ui.py
        │       │   └── video_selection_window.py
        │       ├── main.py
        │       ├── video_edit_window.py
        │       ├── video_editor.py
        │       ├── video_formatter.py
        │       └── video_read.py
        │
        ├── music_player/
        │   ├── gui_window/
        │   │   ├── headers.py
        │   │   ├── player_window.py
        │   │   ├── playlist_picker.py
        │   │   ├── settings.py
        │   │   └── song_window.py
        │   ├── main_window.py
        │   └── player/
        │       ├── player.py
        │       └── player_state.py
        │
        ├── playlist_editor/
        │   └── make_playlist/
        │       ├── control_playlist.py
        │       └── playlist_gui.py
        │
        └── yt_downloader/
            ├── download_thread.py
            └── youtube_downloader.py

---

# Components

MediaCrunch currently consists of four main components:

1. `music_player`
2. `playlist_editor`
3. `yt_downloader`
4. `media_edit`

---

## `music_player`

The music player allows locally stored MP3 files to be played through MediaCrunch.

Once a playlist is selected, the player supports:

- Playing songs using `pygame`
- Pausing playback
- Restarting the current song
- Looping the playlist
- Jumping to the previous song
- Jumping to the next song
- Jumping directly to a song by double-clicking it
- Adjusting volume
- Shuffling and unshuffling the playlist
- Selecting a different playlist

When the playlist reaches the end, playback loops back to the beginning.

---

## `playlist_editor`

The playlist editor allows users to create playlists from songs stored on their computer.

Playlist files store the filepaths of MP3 files in a text file. These playlist files can then be loaded by the `music_player`.

The playlist editor supports:

- Adding individual MP3 files
- Adding entire folders of MP3 files
- Creating playlists for artists, soundtracks, genres, or other collections

Entire folders can be added at once, which is useful when music is already organized into folders.

---

## `yt_downloader`

The YouTube downloader uses `yt-dlp` and FFmpeg to download songs and videos from YouTube.

### Downloading a Single YouTube Video

1. Paste the video's URL.
2. Select either `MP3` or `MP4` as the output format.
3. Select the folder where the file should be saved.
4. Enter the desired output filename.
5. Click **Download**.

The video will be downloaded using the specified filename and output format.

### Downloading a YouTube Playlist

1. Paste the playlist's URL.

   The playlist URL can be obtained by opening the playlist's list of videos on YouTube and clicking the playlist title at the top of the list. The usual YouTube sharing options will be available there.

2. Select either `MP3` or `MP4` as the output format.

3. Select the folder where all of the downloaded videos should be saved.

4. Leave the filename field blank.

   When downloading a playlist, MediaCrunch uses the original YouTube video titles as the filenames.

5. Enable **Numbering** and enter a starting number.

   For example, entering `1` will produce:

       001_Video Title.mp3
       002_Video Title.mp3
       003_Video Title.mp3

   Numbering keeps the files in the same order as the YouTube playlist when they are sorted alphabetically.

   If the folder already contains files numbered through `015_`, entering `16` will continue the numbering:

       016_Video Title.mp3
       017_Video Title.mp3

6. Click **Download**.

MediaCrunch will download the videos in the playlist.

---

## `media_edit`

> **Status: In Development**

The media editor is not fully implemented yet.

The goal of this component is to provide tools for manipulating videos and GIFs while giving the user control over file size and quality.

Planned functionality includes:

- Cropping videos and GIFs
- Changing video resolution
- Changing bitrate
- Reducing file size
- Optimizing media for services with file-size limits
- Other video and GIF manipulation tools

The primary goal is to make it easy to reduce unnecessarily large files while maintaining acceptable visual quality.

---

# Future Development

MediaCrunch is still under development. Planned improvements include:

- More video editing functionality
- GIF editing and cropping
- Improved media compression
- Additional audio and video formats
- Improved playlist management
- Additional YouTube download options
- More cross-platform support
- General GUI improvements