# PlaylistGUI.py
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QFileDialog, QComboBox, QLabel, QMessageBox, QLineEdit, QInputDialog
)
from PyQt5.QtCore import Qt

from src.playlist_editor.make_playlist.control_playlist import ControlPlaylist
from pathlib import Path


class PlaylistGUI(QWidget):
    def __init__(self, config):
        super().__init__()
        self.playlists_dir = config.playlist_folder
        self.songs_dir = config.song_folder
        self.playlist = None   # instance of ControlPlaylist
    

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()

        # self.refreshPlaylistList()

    def _create_widgets(self):
        self.setWindowTitle("Playlist Maker")

        # Playlist selector
        self.playlistLabel = QLabel(f"Selected Playlist: {self.playlist}")
        # self.playlistCombo = QComboBox()
        self.loadPlaylistBtn = QPushButton("Load Playlist")
        self.file_dialog = QFileDialog()
        self.file_dialog.setDirectory(self.playlists_dir)
        self.remove_dialog = QFileDialog()
        self.remove_dialog.setDirectory(self.playlists_dir)

        # self.newPlaylistInput = QLineEdit()
        # self.newPlaylistInput.setPlaceholderText("New playlist name")
        self.createPlaylistBtn = QPushButton("Create a Playlist")
        # self.createPlaylistBtn = QInputDialog()
        self.removePlaylistBtn = QPushButton("Remove a Playlist")
        

        self.trackList = QListWidget()
        self.trackList.setSelectionMode(self.trackList.SingleSelection)

        self.addSongBtn = QPushButton("Add Song")
        self.removeSongBtn = QPushButton("Remove Selected")
        self.upBtn = QPushButton("▲ Move Up")
        self.downBtn = QPushButton("▼ Move Down")
        self.saveBtn = QPushButton("Save Playlist")
        self.addSongBtn = QPushButton("Add Song")
        self.removeSongBtn = QPushButton("Remove Selected")

        self.addFolderBtn = QPushButton("Add Folder")


    def _create_layouts(self):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.playlistLabel)

        # Playlist selection row
        row = QHBoxLayout()
        # row.addWidget(self.playlistLabel)
        # row.addWidget(self.playlistCombo)
        # row.addWidget(self.file_dialog)
        row.addWidget(self.loadPlaylistBtn)

        newRow = QHBoxLayout()
        newRow.addWidget(self.createPlaylistBtn)
        # newRow.addWidget(self.newPlaylistInput)
        newRow.addWidget(self.createPlaylistBtn)
        newRow.addWidget(self.removePlaylistBtn)

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

    def _connect_signals(self):
        # self.playlistCombo.currentIndexChanged.connect(self.loadSelectedPlaylist)
        # self.file_dialog.fileSelected.connect(self.loadSelectedPlaylist)
        self.loadPlaylistBtn.clicked.connect(self.playlist_selection)
        self.file_dialog.fileSelected.connect(self.loadSelectedPlaylist)
        # self.createPlaylistBtn.clicked.connect(self.createPlaylist)
        self.createPlaylistBtn.clicked.connect(self.createPlaylist)
        self.removePlaylistBtn.clicked.connect(self.selectRemovePlaylist)
        self.remove_dialog.fileSelected.connect(self.removePlaylist)
        self.addSongBtn.clicked.connect(self.addSong)
        self.addFolderBtn.clicked.connect(self.addFolder)
        self.removeSongBtn.clicked.connect(self.removeSelected)
        self.upBtn.clicked.connect(self.moveUp)
        self.downBtn.clicked.connect(self.moveDown)
        self.saveBtn.clicked.connect(self.savePlaylist)
        

    # -------------------------
    # LOAD / SAVE LOGIC
    # -------------------------
    # def refreshPlaylistList(self):
    #     self.playlistCombo.clear()
    #     files = [f for f in os.listdir(self.playlists_dir) if f.endswith(".txt")]
    #     self.playlistCombo.addItems(files)

    def playlist_selection(self):
        self.file_dialog.show()

    def loadSelectedPlaylist(self, name):
        basename = Path(name).name
        full_path = os.path.join(self.playlists_dir, name)
        self.playlist = ControlPlaylist(full_path, self.songs_dir)
        self.playlistLabel.setText(f"Selected Playlist: {basename}")

        self.refreshTrackList()

    def refreshTrackList(self):
        self.trackList.clear()

        if self.playlist:
            for t in self.playlist.tracks:
                basename = Path(t).name
                # self.trackList.addItem(t)
                self.trackList.addItem(basename)


    def createPlaylist(self):
        name, ok = QInputDialog.getText(
            self,
            "New Playlist",
            "Enter playlist name:"
        )

        if not ok:
            return

        name = name.strip()

        if not name:
            QMessageBox.warning(
                self,
                "Error",
                "Please enter a valid playlist name."
            )
            return

        if name.lower().endswith(".txt"):
            name = name[:-4]

        # Make sure playlist directory exists
        os.makedirs(self.playlists_dir, exist_ok=True)

        filename = f"{name}.txt"
        full_path = os.path.join(self.playlists_dir, filename)

        if os.path.exists(full_path):
            QMessageBox.warning(
                self,
                "Exists",
                "Playlist already exists."
            )
            return

        try:
            with open(full_path, "w") as f:
                pass
        except OSError as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not create playlist:\n{e}"
            )
            return

        self.playlist = ControlPlaylist(full_path, self.songs_dir)
        self.refreshTrackList()

    def selectRemovePlaylist(self):
        self.remove_dialog.show()
    
    def removePlaylist(self, filepath):
        basename = Path(filepath).name
        Path(filepath).unlink()
        QMessageBox.information(None, "Success", f"Deleted {basename}")
        if self.playlist != None:
            if self.playlist.playlist_path == basename:
                self.playlist = None



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
        self.savePlaylist()
        self.refreshTrackList()

    def removeSelected(self):
        row = self.trackList.currentRow()
        if row < 0:
            return

        self.playlist.remove_track(row)
        self.savePlaylist()
        self.refreshTrackList()

    def moveUp(self):
        row = self.trackList.currentRow()
        if row > 0:
            self.playlist.move_track(row, row - 1)
            self.refreshTrackList()
            self.trackList.setCurrentRow(row - 1)
        self.savePlaylist()

    def moveDown(self):
        row = self.trackList.currentRow()
        if row < self.trackList.count() - 1:
            self.playlist.move_track(row, row + 1)
            self.refreshTrackList()
            self.trackList.setCurrentRow(row + 1)
        self.savePlaylist()

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
        
        self.savePlaylist()
        self.refreshTrackList()



    # -------------------------
    # SAVE PLAYLIST
    # -------------------------
    def savePlaylist(self):
        if self.playlist:
            self.playlist.save()
            # QMessageBox.information(self, "Saved", "Playlist saved successfully!")
