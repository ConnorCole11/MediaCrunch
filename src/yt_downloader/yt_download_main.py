import sys
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from src.yt_downloader.download_thread import DownloadThread as DT
from src.yt_downloader.youtube_downloader import YouTubeDownloader as YDL


def ytDownload_main():
    app = QApplication(sys.argv)
    window = YDL()
    window.show()
    sys.exit(app.exec())

