try: 
    from config_local import Config 
except ImportError: 
    from config import Config

from music.makePlaylist.main import makePlaylist_main
from music.musicPlayer.main import musicPlayer_main
from ytDownload.main import ytDownload_main
# mediaEdit is not yet implemented


# makePlaylist_main(config)
# musicPlayer_main(config)
# ytDownload_main()

# main.py (top-level entry point)
import sys
from PyQt5.QtWidgets import QApplication
from MasterGUI import TopLevelGUI  # This is the master GUI with sidebar & playlist selector

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the master GUI
    config = Config()
    window = TopLevelGUI(config)
    window.show()

    sys.exit(app.exec())
