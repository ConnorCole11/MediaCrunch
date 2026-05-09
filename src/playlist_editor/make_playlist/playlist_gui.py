# PlaylistGUI.py
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QFileDialog, QComboBox, QLabel, QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt

from src.playlist_editor.make_playlist.control_playlist import ControlPlaylist


class PlaylistGUI(QWidget):
    def __init__(self, config):
        super().__init__()
        self.playlists_dir = config.playlist_folder
        self.songs_dir = config.song_folder
        self.playlist = None   # instance of ControlPlaylist

        self.initWidgets()
        self.initLayout()
        self.initBuild()

        self.refreshPlaylistList()

    # -------------------------
    # WIDGET SETUP
    # -------------------------
    def initWidgets(self):
        self.setWindowTitle("Playlist Maker")

        # Playlist selector
        self.playlistLabel = QLabel("Playlist:")
        self.playlistCombo = QComboBox()

        self.newPlaylistInput = QLineEdit()
        self.newPlaylistInput.setPlaceholderText("New playlist name")
        self.createPlaylistBtn = QPushButton("Create")

        # Track list viewer
        self.trackList = QListWidget()
        self.trackList.setSelectionMode(self.trackList.SingleSelection)

        # Buttons
        self.addSongBtn = QPushButton("Add Song")
        self.removeSongBtn = QPushButton("Remove Selected")
        self.upBtn = QPushButton("▲ Move Up")
        self.downBtn = QPushButton("▼ Move Down")
        self.saveBtn = QPushButton("Save Playlist")
        self.addSongBtn = QPushButton("Add Song")
        self.removeSongBtn = QPushButton("Remove Selected")

        self.addFolderBtn = QPushButton("Add Folder")


    # -------------------------
    # LAYOUT SETUP
    # -------------------------
    def initLayout(self):
        mainLayout = QVBoxLayout()

        # Playlist selection row
        row = QHBoxLayout()
        row.addWidget(self.playlistLabel)
        row.addWidget(self.playlistCombo)

        newRow = QHBoxLayout()
        newRow.addWidget(self.newPlaylistInput)
        newRow.addWidget(self.createPlaylistBtn)

        # Track control buttons
        controlRow = QHBoxLayout()
        controlRow.addWidget(self.addSongBtn)
        controlRow.addWidget(self.addFolderBtn)  
        controlRow.addWidget(self.removeSongBtn)
        controlRow.addWidget(self.upBtn)
        controlRow.addWidget(self.downBtn)

        # Final layout assembly
        mainLayout.addLayout(row)
        mainLayout.addLayout(newRow)
        mainLayout.addWidget(self.trackList)
        mainLayout.addLayout(controlRow)
        mainLayout.addWidget(self.saveBtn)

        self.setLayout(mainLayout)

    # -------------------------
    # SIGNALS & CALLBACKS
    # -------------------------
    def initBuild(self):
        self.playlistCombo.currentIndexChanged.connect(self.loadSelectedPlaylist)
        self.createPlaylistBtn.clicked.connect(self.createPlaylist)
        self.addSongBtn.clicked.connect(self.addSong)
        self.addFolderBtn.clicked.connect(self.addFolder)
        self.removeSongBtn.clicked.connect(self.removeSelected)
        self.upBtn.clicked.connect(self.moveUp)
        self.downBtn.clicked.connect(self.moveDown)
        self.saveBtn.clicked.connect(self.savePlaylist)
        

    # -------------------------
    # LOAD / SAVE LOGIC
    # -------------------------
    def refreshPlaylistList(self):
        self.playlistCombo.clear()
        files = [f for f in os.listdir(self.playlists_dir) if f.endswith(".txt")]
        self.playlistCombo.addItems(files)

    def loadSelectedPlaylist(self):
        name = self.playlistCombo.currentText()
        if not name:
            return

        full_path = os.path.join(self.playlists_dir, name)
        self.playlist = ControlPlaylist(full_path, self.songs_dir)

        self.refreshTrackList()

    def refreshTrackList(self):
        self.trackList.clear()
        if self.playlist:
            for t in self.playlist.tracks:
                self.trackList.addItem(t)

    # -------------------------
    # CREATE NEW PLAYLIST
    # -------------------------
    def createPlaylist(self):
        name = self.newPlaylistInput.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a playlist name.")
            return

        filename = f"{name}_Playlist.txt"
        full_path = os.path.join(self.playlists_dir, filename)

        if os.path.exists(full_path):
            QMessageBox.warning(self, "Exists", "Playlist already exists.")
            return

        # Create empty playlist
        open(full_path, "w").close()

        self.refreshPlaylistList()

        # Select it
        index = self.playlistCombo.findText(filename)
        if index >= 0:
            self.playlistCombo.setCurrentIndex(index)

    # -------------------------
    # MODIFY PLAYLIST CONTENT
    # -------------------------
    def addSong(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Song",
            self.songs_dir,
            "Audio Files (*.mp3 *.wav)"
        )
        if not file_path:
            return

        self.playlist.add_track(file_path)
        self.refreshTrackList()

    def removeSelected(self):
        row = self.trackList.currentRow()
        if row < 0:
            return

        self.playlist.remove_track(row)
        self.refreshTrackList()

    def moveUp(self):
        row = self.trackList.currentRow()
        if row > 0:
            self.playlist.move_track(row, row - 1)
            self.refreshTrackList()
            self.trackList.setCurrentRow(row - 1)

    def moveDown(self):
        row = self.trackList.currentRow()
        if row < self.trackList.count() - 1:
            self.playlist.move_track(row, row + 1)
            self.refreshTrackList()
            self.trackList.setCurrentRow(row + 1)

    def addFolder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            self.songs_dir
        )

        if not folder_path:
            return

        # Ensure folder is inside songs_dir
        try:
            _ = os.path.relpath(folder_path, self.songs_dir)
        except ValueError:
            QMessageBox.warning(self, "Invalid Folder",
                                "Please select a folder inside the songs directory.")
            return

        # --- SORT HERE ---
        # Get all audio files, sorted alphabetically
        audio_files = sorted(
            f for f in os.listdir(folder_path)
            if f.lower().endswith((".mp3", ".wav"))
        )

        # Add them in sorted order
        for filename in audio_files:
            full_path = os.path.join(folder_path, filename)
            self.playlist.add_track(full_path)

        self.refreshTrackList()



    # -------------------------
    # SAVE PLAYLIST
    # -------------------------
    def savePlaylist(self):
        if self.playlist:
            self.playlist.save()
            QMessageBox.information(self, "Saved", "Playlist saved successfully!")
