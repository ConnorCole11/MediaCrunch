# TopLevelGUI.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QListWidget, QHBoxLayout, QStackedWidget
)

from src.music_player.gui_window.main_window import PlayerWindow
from src.music_player.gui_window.playlist_picker import PlaylistPicker
from src.playlist_editor.make_playlist.playlist_gui import PlaylistGUI
from src.yt_downloader.youtube_downloader import YouTubeDownloader
from src.media_edit.video_edit.gui.config_ui import ConfigUI


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
            "mediaEdit"
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
        self.playlist_selector = PlaylistPicker(config.playlist_folder)
        self.plistmaker = PlaylistGUI(config)
        self.ytDownloader = YouTubeDownloader()
        self.mediaEditor = ConfigUI()

        self.player_gui = None  # 🔑 IMPORTANT: persistent PlayerWindow

        # ------------------
        # Add initial widgets
        # ------------------
        self.stack.addWidget(self.playlist_selector)  # index 0
        self.stack.addWidget(self.plistmaker)         # index 1
        self.stack.addWidget(self.ytDownloader)       # index 2
        self.stack.addWidget(self.mediaEditor)        # index 3

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
