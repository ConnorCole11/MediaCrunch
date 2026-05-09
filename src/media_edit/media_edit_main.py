from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLabel,
    QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QPushButton, QVBoxLayout, QFileDialog
)
from src.media_edit.video_edit.video_edit_window import VideoEditWindow
import sys



if __name__ == "__main__":
    app = QApplication(sys.argv)

    editor = VideoEditWindow()
    editor.show()

    sys.exit(app.exec_())