from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLabel,
    QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QPushButton, QVBoxLayout, QFileDialog
)
import sys
import os
from VideoFormatter.VideoFormatter import MP4matter
from VideoEditor.VideoEditor import VideoEditor

class ConfigUI(QWidget):
    """
    Dynamically builds a configuration form from PARAMS metadata.
    Add or remove parameters in PARAMS — the GUI updates automatically.
    """

    PARAMS = {
        "bitrate": {"type": "text", "label": "Bitrate (e.g. 2M)", "default": "2M"},
        "fps": {"type": "number", "label": "FPS", "default": 30, "min": 1, "max": 240},
        "width": {"type": "number", "label": "Width", "default": 1920, "min": 1, "max": 8192},
        "height": {"type": "number", "label": "Height", "default": 1080, "min": 1, "max": 8192},
        "preset": {"type": "choice", "label": "Encoding Preset",
                   "options": ["ultrafast", "fast", "medium", "slow"], "default": "medium"}
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Config")
        self.widgets = {}
        self.input_path = None

        self.init_ui()

    def init_ui(self):
        self.init_widgets()
        self.init_layouts()
        self.init_connections()

    def init_widgets(self):
        # create dynamic widgets from PARAMS
        self.form_widgets = {}  # store widgets for layout
        
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
                for option in meta.get("options", []):
                    w.addItem(option)
                w.setCurrentText(meta["default"])

            self.widgets[name] = w  # store for config use
            self.form_widgets[name] = (QLabel(meta["label"]), w)

        # standalone buttons
        self.file_button = QPushButton("Select Video File")
        self.output_button = QPushButton("Select Output Title")
        self.apply_button = QPushButton("Apply Settings")

    def init_layouts(self):
        main = QVBoxLayout()
        form = QFormLayout()

        # add dynamic form inputs
        for label, widget in self.form_widgets.values():
            form.addRow(label, widget)

        main.addLayout(form)
        main.addWidget(self.file_button)
        main.addWidget(self.output_button)
        main.addWidget(self.apply_button)

        self.setLayout(main)

    def init_connections(self):
        self.file_button.clicked.connect(self._select_input)
        self.output_button.clicked.connect(self._select_output)
        self.apply_button.clicked.connect(self._on_apply)

    def _on_apply(self):
        if not self.input_path:
            print("No input file selected!")
            return

        values = self.get_values()
        print("Current Config:", values)

        try:
            # Ensure MP4-safe file
            mp4 = MP4matter(self.input_path)
            safe_path = mp4.filedir

            # Load editor
            editor = VideoEditor(safe_path)

            # Run reencode
            if os.path.exists(self.outputPath):
                output_path = self.outputPath
            else:
                raise ValueError("outputPath was not defined.")
            
            editor.reencode(
                output_path=output_path,
                bitrate=values["bitrate"],
                fps=values["fps"],
                width=values["width"],
                height=values["height"],
                preset=values["preset"]
            )

            print("Saved:", output_path)
            editor.close()

        except Exception as e:
            print("Error:", e)


    def get_values(self) -> dict:
        """Return all current parameter values from widgets."""
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
    
    def _select_input(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.mov *.avi *.mkv *.m4v);;All Files (*)"
        )

        if filepath:
            # Store the selected path
            self.input_path = filepath
            print("Selected file:", filepath)

    def _select_output(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Select Output File",
            "",
            "MP4 Files (*.mp4);;All Files (*)"
        )

        if filepath:
            self.outputPath = filepath
            print("Output file:", filepath)



    def run(self):
        app = QApplication(sys.argv)
        # ui = ConfigUI()
        self.show()
        sys.exit(app.exec())
