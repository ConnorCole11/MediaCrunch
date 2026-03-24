from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QBrush
import os

class SongWindow(QWidget):
    songSelected = pyqtSignal(int)  # emitted when user double-clicks a song

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.highlight_color = "#00CCFF"

        self.playlist = QListWidget()
        self.populate_songs()

        layout = QVBoxLayout(self)
        layout.addWidget(self.playlist)

        # connect double-click
        self.playlist.itemDoubleClicked.connect(self.handle_double_click)

        # connect to Player signals
        self.player.songChanged.connect(self.highlight_current_song)

    def populate_songs(self):
        self.playlist.clear()
        for s in self.player.normal_song_dirs:
            self.playlist.addItem(os.path.basename(s))

    def handle_double_click(self, item):
        """Emit a signal when song is double clicked."""
        # emit the index to PlayerWindow
        index = self.playlist.row(item)
        self.songSelected.emit(index)

    # SongWindow.py
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

    # SongWindow.py
    def set_songs(self, song_list):
        """Replace the QListWidget items with the new song order"""
        self.playlist.clear()
        for s in song_list:
            self.playlist.addItem(os.path.basename(s))