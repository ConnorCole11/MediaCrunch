import sys
import os
import pygame
from PyQt5.QtWidgets import QApplication
from GuiWindow.MainWindow import PlayerWindow  # your new GUI class
import argparse
import config


def parse_args():
    parser = argparse.ArgumentParser(
        description="Play music from a playlist file."
    )

    parser.add_argument(
        "--Playlist",
        type=str,
        required=True,
        help="Name of the playlist file (e.g., 'rock.txt')."
    )

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()
    plist_txt = args.Playlist
    # Init pygame mixer
    pygame.mixer.init()

    this_dir = os.path.dirname(os.path.abspath(__file__))
    playlist_file = os.path.join(this_dir, config.playlist_folder, plist_txt)
    songs_folder = os.path.join(this_dir, config.songs_folder)

    app = QApplication(sys.argv)

    window = PlayerWindow(
        playlist_file=playlist_file,
        song_folder=songs_folder
    )
    window.show()

    # Run the Qt event loop
    app.exec_()

    pygame.mixer.quit()
    sys.exit(0)
