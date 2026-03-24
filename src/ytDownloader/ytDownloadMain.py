import sys
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from src.ytDownloader.DownloadThread import DownloadThread as DT
from src.ytDownloader.YoutubeDownloader import YouTubeDownloader as YDL


def ytDownload_main():
    app = QApplication(sys.argv)
    window = YDL()
    window.show()
    sys.exit(app.exec())

