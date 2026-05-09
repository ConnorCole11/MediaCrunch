from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLabel,
    QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QPushButton, QVBoxLayout, QFileDialog
)
from PyQt5.QtCore import pyqtSignal
import sys


class VideoSelectionWindow(QWidget):
    """
    The window that pops up when you need to select a
    file. Gives that video's properties to the parameter inputs
    by default.
    """

    file_selected = pyqtSignal(str)  # ✅ signal inside class


    def __init__(self):
        super().__init__()
        self._create_widgets()
        self._create_layouts()
        self._connect_signals()
        self._apply_styles()

    def _get_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "test")

        if file_path:
            self.file_selected.emit(file_path)
    
    def _create_widgets(self):
        """Create all of the widgets for video selection."""
        self.select_vid = QPushButton("Select Video to Edit")

    def _create_layouts(self):
        self.selection_box = QVBoxLayout()
        self.selection_box.addWidget(self.select_vid)
        self.setLayout(self.selection_box)

    def _connect_signals(self):
        self.select_vid.clicked.connect(self._get_file)

    def _apply_styles(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    selector = VideoSelectionWindow()
    selector.show()

    sys.exit(app.exec_())