import sys
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from src.yt_downloader.download_thread import DownloadThread as DT

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(200, 200, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # --- URL ---
        url_layout = QHBoxLayout()
        url_label = QLabel("YouTube URL:")
        self.url_input = QLineEdit()
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)

        # --- File Type ---
        type_layout = QHBoxLayout()
        type_label = QLabel("Format:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["mp4", "mp3"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)

        # --- Folder ---
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Target Folder:")
        self.folder_input = QLineEdit()
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_btn)

        # --- File Name ---
        name_layout = QHBoxLayout()
        name_label = QLabel("Filename:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)

        # --- Numbering ---
        num_layout = QHBoxLayout()
        self.num_checkbox = QPushButton("Enable Numbering")
        self.num_checkbox.setCheckable(True)

        self.start_number_input = QLineEdit()
        self.start_number_input.setPlaceholderText("Start at (e.g. 001)")
        self.start_number_input.setFixedWidth(100)

        num_layout.addWidget(self.num_checkbox)
        num_layout.addWidget(self.start_number_input)

        layout.addLayout(num_layout)

        # --- Download Button ---
        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.start_download)

        # --- Log Output ---
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Download logs will appear here...")

        # Add all to layout
        layout.addLayout(url_layout)
        layout.addLayout(type_layout)
        layout.addLayout(folder_layout)
        layout.addLayout(name_layout)
        layout.addWidget(self.download_btn)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.folder_input.setText(folder)

    def start_download(self):
        url = self.url_input.text().strip()
        folder = self.folder_input.text().strip()
        name = self.name_input.text().strip() or None
        filetype = self.type_combo.currentText()

        if not url or not folder:
            QMessageBox.warning(self, "Input Error", "URL and folder are required.")
            return

        output_path = self.build_output_path(folder, name)

        # Determine autonumber start value
        autonum = None
        if self.num_checkbox.isChecked():
            start = self.start_number_input.text().strip()
            autonum = int(start) if start.isdigit() else 1

        self.download_btn.setEnabled(False)
        self.log_output.clear()
        self.log_output.append("Starting download...\n")

        # PASS autonumber_start HERE
        self.thread = DT(
            url,
            output_path,
            filetype,
            cookies_path='cookies.txt',
            autonumber_start=autonum
        )

        self.thread.log.connect(self.update_log)
        self.thread.done.connect(self.download_finished)
        self.thread.start()


    def build_output_path(self, folder: str, name: str = None):
        folder_path = Path(folder).resolve()
        folder_path.mkdir(parents=True, exist_ok=True)

        # If numbering is enabled
        if self.num_checkbox.isChecked():
            start = self.start_number_input.text().strip()

            if not start.isdigit():
                start = "1"

            # Always use 3 digits
            self.numbering_index = int(start)
            self.numbering_width = 3

            filename = "%(autonumber)03d %(title)s.%(ext)s"
            return str(folder_path / filename)

        # Default behavior
        filename = name if name else "%(title)s.%(ext)s"
        return str(folder_path / filename)

    def update_log(self, message):
        self.log_output.append(message)

    def download_finished(self, success):
        self.download_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, "Download Complete", "Download finished successfully!")
        else:
            QMessageBox.critical(self, "Download Failed", "There was an error downloading the video.")