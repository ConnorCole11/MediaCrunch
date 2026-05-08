import sys
from PyQt5.QtWidgets import QApplication
from src.mediaEdit.videoEdit.ConfigQT.ConfigQT import ConfigUI
from src.mediaEdit.videoEdit.VideoEditor.VideoEditor import VideoEditor
from src.mediaEdit.videoEdit.VideoFormatter.VideoFormatter import MP4matter

def main():
    app = QApplication(sys.argv)

    config = ConfigUI()
    config.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    print("Running")
    main()