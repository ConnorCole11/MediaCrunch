try: 
    from config_local import Config 
except ImportError: 
    from config import Config

from src.playlist_editor.make_playlist.playlist_maker_main import makePlaylist_main
from src.music_player.music_player_main import musicPlayer_main
from src.yt_downloader.yt_download_main import ytDownload_main
# mediaEdit is not yet implemented


# makePlaylist_main(config)
# musicPlayer_main(config)
# ytDownload_main()

# main.py (top-level entry point)
import sys
from PyQt5.QtWidgets import QApplication
from src.master_gui import TopLevelGUI  # This is the master GUI with sidebar & playlist selector

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the master GUI
    config = Config()
    window = TopLevelGUI(config)
    window.show()

    sys.exit(app.exec())
