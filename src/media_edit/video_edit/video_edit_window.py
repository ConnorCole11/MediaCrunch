from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QStackedWidget
)
import sys
import os
from src.media_edit.video_edit.gui.video_selection_window import VideoSelectionWindow
from src.media_edit.video_edit.gui.config_ui import ConfigUI

class VideoEditWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()

        self.selection_screen = VideoSelectionWindow()

        self.stack.addWidget(self.selection_screen)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)

        self.setLayout(layout)

        self.selection_screen.file_selected.connect(
            self.open_editor
        )

    def open_editor(self, filepath):

        self.editor_screen = ConfigUI(filepath)

        self.stack.addWidget(self.editor_screen)

        self.stack.setCurrentWidget(self.editor_screen)