import sys
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit,
    QFileDialog, QMessageBox
)

from src.yt_downloader.download_thread import DownloadThread as DT


class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(200, 200, 600, 400)

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()

    def _create_widgets(self):
        # URL
        self.url_label = QLabel("YouTube URL:")
        self.url_input = QLineEdit()

        # File Type
        self.type_label = QLabel("Format:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["mp4", "mp3"])
        self.type_combo.setFixedWidth(600)

        # Folder
        self.folder_label = QLabel("Target Folder:")
        self.folder_input = QLineEdit()
        self.browse_btn = QPushButton("Browse")

        # File Name
        self.name_label = QLabel("Filename:")
        self.name_input = QLineEdit()

        # Numbering
        self.num_checkbox = QPushButton("Enable Numbering (for playlist downloads)")
        # self.num_checkbox.setFixedWidth(400)
        self.num_checkbox.setCheckable(True)

        self.start_number_input = QLineEdit()
        self.start_number_input.setPlaceholderText("(e.g. Enter '1' to add 001_ 002_ filename prefixes)")
        # self.start_number_input.setFixedWidth(150)

        # Download
        self.download_btn = QPushButton("Download")

        # Log
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText(
            "Download logs will appear here..."
        )

    def _create_layouts(self):
        main_layout = QVBoxLayout()

        # URL
        url_layout = QHBoxLayout()
        url_layout.addWidget(self.url_label)
        url_layout.addWidget(self.url_input)

        # File Type
        type_layout = QHBoxLayout()
        type_layout.addWidget(self.type_label)
        type_layout.addWidget(self.type_combo)

        # Folder
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(self.browse_btn)

        # File Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)

        # Numbering
        num_layout = QHBoxLayout()
        num_layout.addWidget(self.num_checkbox)
        num_layout.addWidget(self.start_number_input)

        # Main layout
        main_layout.addLayout(url_layout)
        main_layout.addLayout(type_layout)
        main_layout.addLayout(folder_layout)
        main_layout.addLayout(name_layout)
        main_layout.addLayout(num_layout)
        main_layout.addWidget(self.download_btn)
        main_layout.addWidget(self.log_output)

        self.setLayout(main_layout)

    def _connect_signals(self):
        self.browse_btn.clicked.connect(self.browse_folder)
        self.download_btn.clicked.connect(self.start_download)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder"
        )

        if folder:
            self.folder_input.setText(folder)

    def start_download(self):
        url = self.url_input.text().strip()
        folder = self.folder_input.text().strip()
        name = self.name_input.text().strip() or None
        filetype = self.type_combo.currentText()

        if not url or not folder:
            QMessageBox.warning(
                self,
                "Input Error",
                "URL and folder are required."
            )
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

        self.thread = DT(
            url,
            output_path,
            filetype,
            cookies_path="cookies.txt",
            autonumber_start=autonum
        )

        self.thread.log.connect(self.update_log)
        self.thread.done.connect(self.download_finished)

        self.thread.start()

    def build_output_path(self, folder: str, name: str = None):
        folder_path = Path(folder).resolve()
        folder_path.mkdir(parents=True, exist_ok=True)

        if self.num_checkbox.isChecked():
            start = self.start_number_input.text().strip()

            if not start.isdigit():
                start = "1"

            self.numbering_index = int(start)
            self.numbering_width = 3

            filename = "%(autonumber)03d %(title)s.%(ext)s"

            return str(folder_path / filename)

        filename = name if name else "%(title)s.%(ext)s"

        return str(folder_path / filename)

    def update_log(self, message):
        self.log_output.append(message)

    def download_finished(self, success):
        self.download_btn.setEnabled(True)

        if success:
            QMessageBox.information(
                self,
                "Download Complete",
                "Download finished successfully!"
            )
        else:
            QMessageBox.critical(
                self,
                "Download Failed",
                "There was an error downloading the video."
            )