from PyQt5.QtWidgets import QApplication
from music.musicPlayer.GuiWindow.MainWindow import PlayerWindow  # your new GUI class
import sys
import os
import pygame
import argparse


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


def musicPlayer_main(config):
    args = parse_args()
    plist_txt = args.Playlist
    # Init pygame mixer
    pygame.mixer.init()

    this_dir = os.path.dirname(os.path.abspath(__file__))
    playlist_file = os.path.join(this_dir, config.playlist_folder, plist_txt)
    songs_folder = os.path.join(this_dir, config.song_folder)

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
