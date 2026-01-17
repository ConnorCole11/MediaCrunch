# main.py
import sys
from PyQt5.QtWidgets import QApplication
from PlaylistGUI.PlaylistGUI import PlaylistGUI

def makePlaylist_main():
    app = QApplication(sys.argv)

    playlists_dir = "../Playlists"
    songs_dir = "../../storage/songs"

    window = PlaylistGUI(playlists_dir, songs_dir)
    window.resize(600, 500)
    window.show()

    sys.exit(app.exec_())
