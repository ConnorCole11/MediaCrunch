# TopLevelGUI.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QListWidget, QHBoxLayout, QStackedWidget
)

from music.musicPlayer.GuiWindow.MainWindow import PlayerWindow
from music.musicPlayer.GuiWindow.PlaylistPicker import PlaylistPicker
from music.makePlaylist.PlaylistGUI.PlaylistGUI import PlaylistGUI
from ytDownload.YoutubeDownloader.YoutubeDownloader import YouTubeDownloader
# from GUI4.MainWindow import GUI4Window


class TopLevelGUI(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setWindowTitle("Master GUI")

        self.config = config

        # ------------------
        # Sidebar
        # ------------------
        self.sidebar = QListWidget()
        self.sidebar.addItems([
            "Music Player",
            "Playlist Maker",
            "ytDownloader",
            "mediaEdit (not implemented)"
        ])
        self.sidebar.setFixedWidth(200)
        self.sidebar.currentRowChanged.connect(self.switch_gui)

        # ------------------
        # Central stack
        # ------------------
        self.stack = QStackedWidget()

        # ------------------
        # Sub-GUIs
        # ------------------
        self.playlist_selector = PlaylistPicker()
        self.plistmaker = PlaylistGUI(config)
        self.ytDownloader = YouTubeDownloader()
        # self.gui4 = GUI4Window()

        self.player_gui = None  # 🔑 IMPORTANT: persistent PlayerWindow

        # ------------------
        # Add initial widgets
        # ------------------
        self.stack.addWidget(self.playlist_selector)  # index 0
        self.stack.addWidget(self.plistmaker)         # index 1
        self.stack.addWidget(self.ytDownloader)       # index 2
        # self.stack.addWidget(self.gui4)              # index 3

        # ------------------
        # Layout
        # ------------------
        layout = QHBoxLayout(self)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)
        self.setLayout(layout)

        # ------------------
        # Signals
        # ------------------
        self.playlist_selector.playlistSelected.connect(
            self.launch_player_window
        )

        # Start with Music Player tab
        self.sidebar.setCurrentRow(0)

    # ======================================================
    # Sidebar routing (STATE-AWARE)
    # ======================================================
    def switch_gui(self, index):
        # Music Player
        if index == 0:
            if self.player_gui is not None:
                self.stack.setCurrentWidget(self.player_gui)
            else:
                self.stack.setCurrentWidget(self.playlist_selector)
        else:
            self.stack.setCurrentIndex(index)

    # ======================================================
    # Player launcher
    # ======================================================
    def launch_player_window(self, playlist_path):
        """Called once when playlist is selected"""

        if self.player_gui is None:
            self.player_gui = PlayerWindow(
                playlist_path,
                self.config.song_folder
            )
            self.stack.addWidget(self.player_gui)

        self.stack.setCurrentWidget(self.player_gui)
