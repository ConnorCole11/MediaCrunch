# main.py
import sys
from PyQt5.QtWidgets import QApplication
from music.makePlaylist.PlaylistGUI.PlaylistGUI import PlaylistGUI

def makePlaylist_main(config):
    app = QApplication(sys.argv)

    playlists_dir = config.playlist_folder
    songs_dir = config.song_folder

    window = PlaylistGUI(playlists_dir, songs_dir)
    window.resize(600, 500)
    window.show()

    sys.exit(app.exec_())
