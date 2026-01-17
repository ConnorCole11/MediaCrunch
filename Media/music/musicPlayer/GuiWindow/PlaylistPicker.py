# PlaylistPicker.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import pyqtSignal

class PlaylistPicker(QWidget):
    # Signal to send the selected playlist path back to the launcher
    playlistSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.selected_playlist = None

        # Label to show current selection
        self.label = QLabel("No playlist selected")
        self.btn_select = QPushButton("Select Playlist")
        self.btn_confirm = QPushButton("Confirm")
        self.btn_confirm.setEnabled(False)  # Disabled until a file is selected

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select)
        layout.addWidget(self.btn_confirm)

        # Connections
        self.btn_select.clicked.connect(self.choose_file)
        self.btn_confirm.clicked.connect(self.confirm_selection)

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Playlist File", "", "Text Files (*.txt);;All Files (*)")
        if path:
            self.selected_playlist = path
            self.label.setText(f"Selected: {path}")
            self.btn_confirm.setEnabled(True)

    def confirm_selection(self):
        if self.selected_playlist:
            self.playlistSelected.emit(self.selected_playlist)