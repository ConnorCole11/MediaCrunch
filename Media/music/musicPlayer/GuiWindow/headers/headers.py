from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Headers(QWidget):
    """
    Displays song title, paused state, and loop state.
    """

    def __init__(self):
        super().__init__()

        self.title = QLabel("No song selected. Select a song by double clicking.")
        self.paused = QLabel("Paused: ❌")
        self.looped = QLabel("Loop: ❌")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.paused)
        self.layout.addWidget(self.looped)

    # slots (methods receiving signals)
    def set_title(self, name):
        self.title.setText(f"Song: {name}")

    def set_paused(self, paused: bool):
        self.paused.setText(f"Paused: {'✅' if paused else '❌'}")

    def set_loop(self, looped: bool):
        self.looped.setText(f"Loop: {'✅' if looped else '❌'}")