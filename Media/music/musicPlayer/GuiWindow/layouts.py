# Layouts.py
from PyQt5.QtWidgets import QVBoxLayout

def build_main_layout(status_widget, playlist_widget, controls_widget, volume_widget):
    layout = QVBoxLayout()
    layout.addWidget(status_widget)
    layout.addWidget(playlist_widget)
    layout.addWidget(controls_widget)
    layout.addWidget(volume_widget)
    return layout
