# TopLevelGUI.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QListWidget, QHBoxLayout, QStackedWidget
)

from src.music_player.main_window import MainPlayerWindow
from src.playlist_editor.make_playlist.playlist_gui import PlaylistGUI
from src.yt_downloader.youtube_downloader import YouTubeDownloader
from src.media_edit.video_edit.gui.config_ui import ConfigUI


class TopLevelGUI(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setWindowTitle("Master GUI")

        self.config = config
        
        self._create_widgets()
        self._create_layouts()
        self._connect_signals()
        self._configure_appearance()

    def _create_widgets(self):

        self.sidebar = QListWidget()
        self.sidebar.addItems([
            "Music Player",
            "Playlist Maker",
            "ytDownloader",
            "mediaEdit"
        ])
        self.sidebar.setFixedWidth(200)

        self.main_player_window = MainPlayerWindow(self.config)
        self.plistmaker = PlaylistGUI(self.config)
        self.ytDownloader = YouTubeDownloader()
        self.mediaEditor = ConfigUI()

        # Start with Music Player tab
        self.sidebar.setCurrentRow(0)

    def _create_layouts(self):
        self.stack = QStackedWidget()
        self.stack.addWidget(self.main_player_window) # index 0
        self.stack.addWidget(self.plistmaker)         # index 1
        self.stack.addWidget(self.ytDownloader)       # index 2
        self.stack.addWidget(self.mediaEditor)        # index 3

        layout = QHBoxLayout(self)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def _connect_signals(self):
        self.sidebar.currentRowChanged.connect(self.switch_gui)

    def _configure_appearance(self):
        self.sidebar.setFixedWidth(200)


    # ======================================================
    # Sidebar routing (STATE-AWARE)
    # ======================================================
    def switch_gui(self, index):
        self.stack.setCurrentIndex(index)