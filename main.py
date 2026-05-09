try: 
    from config_local import Config 
except ImportError: 
    from config import Config

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
