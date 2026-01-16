import sys
from PyQt5.QtWidgets import QApplication
from ConfigQT.ConfigQT import ConfigUI
from VideoEditor.VideoEditor import VideoEditor
from VideoFormatter.VideoFormatter import MP4matter

def main():
    app = QApplication(sys.argv)

    config = ConfigUI()
    config.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()