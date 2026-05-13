from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QListWidgetItem
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QBrush
import os

class SongWindow(QWidget):
    songClicked = pyqtSignal(str)  # emitted when user double-clicks a song

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.highlight_color = "#00CCFF"

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()

    def _create_widgets(self):
        self.playlist = QListWidget()
        self._populate_songs()

    def _create_layouts(self):
        self.my_layout = QVBoxLayout(self)
        self.my_layout.addWidget(self.playlist)

    def _connect_signals(self):
        self.playlist.itemDoubleClicked.connect(self.handle_double_click)
        self.player.songChanged.connect(self.highlight_current_song)

    def _populate_songs(self):
        """Fill playlist QListWidget object with song buttons."""
        self.playlist.clear()
        for s in self.player.song_dirs:  # use current list
            item = QListWidgetItem(os.path.basename(s))
            item.setData(1, s)  # store full path (Qt.UserRole = 1)
            self.playlist.addItem(item)

    def handle_double_click(self, item):
        song_path = item.data(1)  # 🔥 get actual stored path
        self.songClicked.emit(song_path)

    def highlight_current_song(self, index):
        if not (0 <= index < len(self.player.song_dirs)):
            return

        current_song_name = os.path.basename(self.player.song_dirs[index])

        for i in range(self.playlist.count()):
            item = self.playlist.item(i)
            item.setBackground(QBrush(QColor("white")))  # reset

            if item.text() == current_song_name:
                item.setBackground(QBrush(QColor(self.highlight_color)))
                self.playlist.setCurrentRow(i)
                self.playlist.scrollToItem(item)

    def set_songs(self, song_list):
        self.playlist.clear()
        for s in song_list:
            item = QListWidgetItem(os.path.basename(s))
            item.setData(1, s)
            self.playlist.addItem(item)