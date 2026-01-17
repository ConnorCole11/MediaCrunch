# TopLevelGUI.py
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QHBoxLayout, QStackedWidget
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
        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.addItems(["Music Player", "Playlist Maker", "ytDownloader", "mediaEdit (not implemented)"])
        self.sidebar.setFixedWidth(200)
        self.sidebar.currentRowChanged.connect(self.switch_gui)

        # Central stacked widget
        self.stack = QStackedWidget()

        # Sub-GUIs
        self.playlist_selector = PlaylistPicker()
        self.plistmaker = PlaylistGUI(config)
        self.ytDownloader = YouTubeDownloader()
        # self.gui4 = GUI4Window()

        # Add sub-GUIs to the stack
        self.stack.addWidget(self.playlist_selector)  # index 0
        self.stack.addWidget(self.plistmaker)               # index 1
        self.stack.addWidget(self.ytDownloader)               # index 2
        # self.stack.addWidget(self.gui4)               # index 3

        # Layout
        layout = QHBoxLayout(self)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)
        self.setLayout(layout)

        # Start with first option
        self.sidebar.setCurrentRow(0)

        # Connect playlist selector to launch PlayerWindow
        self.playlist_selector.playlistSelected.connect(self.launch_player_window)

    def switch_gui(self, index):
        self.stack.setCurrentIndex(index)

    def launch_player_window(self, playlist_path):
        """Called when the playlist is selected"""
        # Remove old PlayerWindow if it exists
        if hasattr(self, 'player_gui'):
            self.stack.removeWidget(self.player_gui)
            self.player_gui.deleteLater()

        # Create new PlayerWindow with the selected playlist
        # self.player_gui = PlayerWindow(playlist_path, "songs")
        self.player_gui = PlayerWindow(playlist_path, self.config.song_folder)
        self.stack.addWidget(self.player_gui)
        self.stack.setCurrentWidget(self.player_gui)
