from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QLabel,
    QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QPushButton, QVBoxLayout,
    QApplication
)
import sys
import os

from src.mediaEdit.videoEdit.video_formatter import MP4matter as mp4mat
from src.mediaEdit.videoEdit.video_read import VideoInfo as vinfo
from src.mediaEdit.videoEdit.video_editor import VideoEditor as vedit


class ConfigUI(QWidget):
    """
    Configuration window for a single video.
    This window is created after a video file is selected.
    """

    PARAMS = {
        "bitrate": {"type": "text", "label": "Bitrate (e.g. 2M)", "default": "2M"},
        "fps": {"type": "number", "label": "FPS", "default": 30, "min": 1, "max": 240},
        "width": {"type": "number", "label": "Width", "default": 1920, "min": 1, "max": 8192},
        "height": {"type": "number", "label": "Height", "default": 1080, "min": 1, "max": 8192},
        "preset": {
            "type": "choice",
            "label": "Encoding Preset",
            "options": ["ultrafast", "fast", "medium", "slow"],
            "default": "medium"
        }
    }

    # =====================
    # INIT
    # =====================
    def __init__(self, video_path: str):
        super().__init__()

        self.setWindowTitle("Video Config")

        self.video_path = video_path
        self.output_path = None

        self.widgets = {}
        self.form_widgets = {}

        self.init_widgets()
        self.init_layouts()
        self.init_connections()

        self.load_video_defaults()

    # =====================
    # VIDEO DEFAULTS
    # =====================
    def load_video_defaults(self):
        """Load metadata immediately when window opens."""
        try:
            reader = vinfo(self.video_path)
            reader._get_ffprobe_info()
            reader._parse_info() # adds internal values
            info = reader.summary()
            self.apply_video_defaults(info)

        except Exception as e:
            print("Failed to load video info:", e)

    def apply_video_defaults(self, info: dict):
        video = info.get("video", {})

        # FPS
        if video.get("fps"):
            self.widgets["fps"].setValue(max(1, round(video["fps"])))

        # Resolution
        if video.get("width"):
            self.widgets["width"].setValue(video["width"])

        if video.get("height"):
            self.widgets["height"].setValue(video["height"])

        # Bitrate (THIS is your issue)
        if video.get("bitrate_bps"):
            self.widgets["bitrate"].setText(
                self._format_bitrate(info["video"]["bitrate_bps"])
)

    # =====================
    # WIDGET CREATION
    # =====================
    def init_widgets(self):
        for name, meta in self.PARAMS.items():

            if meta["type"] == "text":
                w = QLineEdit()
                w.setText(meta.get("default", ""))

            elif meta["type"] == "number":
                w = QSpinBox()
                w.setRange(meta.get("min", 0), meta.get("max", 9999))
                w.setValue(meta.get("default", 0))

            elif meta["type"] == "float":
                w = QDoubleSpinBox()
                w.setRange(meta.get("min", 0.0), meta.get("max", 9999.0))
                w.setValue(meta.get("default", 0.0))
                w.setSingleStep(0.1)

            elif meta["type"] == "choice":
                w = QComboBox()
                w.addItems(meta.get("options", []))
                w.setCurrentText(meta.get("default"))

            self.widgets[name] = w
            self.form_widgets[name] = (QLabel(meta["label"]), w)

        # buttons (NO file button anymore)
        self.output_button = QPushButton("Select Output File")
        self.apply_button = QPushButton("Apply Settings")

    # =====================
    # LAYOUT
    # =====================
    def init_layouts(self):
        main = QVBoxLayout()
        form = QFormLayout()

        for label, widget in self.form_widgets.values():
            form.addRow(label, widget)

        main.addLayout(form)
        main.addWidget(self.output_button)
        main.addWidget(self.apply_button)

        self.setLayout(main)

    # =====================
    # SIGNALS
    # =====================
    def init_connections(self):
        self.output_button.clicked.connect(self._select_output)
        self.apply_button.clicked.connect(self._on_apply)

    # =====================
    # OUTPUT FILE
    # =====================
    def _select_output(self):
        from PyQt5.QtWidgets import QFileDialog

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Select Output File",
            "",
            "MP4 Files (*.mp4);;All Files (*)"
        )

        if filepath:
            self.output_path = filepath
            print("Output file:", filepath)

    # =====================
    # APPLY
    # =====================
    def _on_apply(self):
        if not self.video_path:
            print("No input file provided!")
            return

        if not self.output_path:
            print("No output file selected!")
            return

        values = self.get_values()
        print("Current Config:", values)

        try:
            mp4 = mp4mat(self.video_path)
            safe_path = mp4.filedir

            editor = vedit(safe_path)

            editor.reencode(
                output_path=self.output_path,
                bitrate=values["bitrate"],
                fps=values["fps"],
                width=values["width"],
                height=values["height"],
                preset=values["preset"]
            )

            print("Saved:", self.output_path)
            editor.close()

        except Exception as e:
            print("Error:", e)

    # =====================
    # UTILS
    # =====================
    def get_values(self) -> dict:
        values = {}

        for name, widget in self.widgets.items():
            if isinstance(widget, QLineEdit):
                values[name] = widget.text()
            elif isinstance(widget, QSpinBox):
                values[name] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                values[name] = widget.value()
            elif isinstance(widget, QComboBox):
                values[name] = widget.currentText()

        return values
    
    def _format_bitrate(self, bps: int) -> str:
        if bps is None:
            return "Unknown"

        units = ["", "K", "M", "G"]
        value = float(bps)
        unit_index = 0

        while value >= 1000 and unit_index < len(units) - 1:
            value /= 1000
            unit_index += 1

        return f"{value:.3g}{units[unit_index]}"

if __name__ == "__main__":
    test_vid_path = "storage/videos/WhatHappenedToMrPuff.mp4"

    app = QApplication(sys.argv)
    config = ConfigUI(test_vid_path)
    config.show()

    sys.exit(app.exec_())
