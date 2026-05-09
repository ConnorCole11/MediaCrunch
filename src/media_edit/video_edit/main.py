import sys
from PyQt5.QtWidgets import QApplication
from src.mediaEdit.videoEdit.gui.config_ui import ConfigUI
from src.mediaEdit.videoEdit.video_editor import VideoEditor
from src.mediaEdit.videoEdit.video_formatter import MP4matter

def main():
    app = QApplication(sys.argv)

    config = ConfigUI()
    config.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    print("Running")
    main()