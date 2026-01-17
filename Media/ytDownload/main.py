import sys
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ytDownload.DownloadThread.DownloadThread import DownloadThread as DT
from ytDownload.YoutubeDownloader.YoutubeDownloader import YouTubeDownloader as YDL


def ytDownload_main():
    app = QApplication(sys.argv)
    window = YDL()
    window.show()
    sys.exit(app.exec())

