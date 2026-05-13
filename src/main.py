try: 
    from config_local import Config 
except ImportError: 
    from config import Config
import pygame
import sys
from PyQt5.QtWidgets import QApplication
from src.master_gui import TopLevelGUI  # This is the master GUI with sidebar & playlist selector
import os

def initialize_folders(config):
    os.makedirs(config.playlist_folder, exist_ok=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pygame.mixer.init()

    # Create the master GUI
    config = Config()
    initialize_folders(config)
    window = TopLevelGUI(config)
    window.show()

    sys.exit(app.exec())
