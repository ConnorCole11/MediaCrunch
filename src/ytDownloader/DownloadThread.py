import sys
import subprocess
from pathlib import Path
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class DownloadThread(QThread):
    log = pyqtSignal(str)
    done = pyqtSignal(bool)

    def __init__(self, url, output_path, filetype, cookies_path, autonumber_start=None):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.filetype = filetype
        self.cookies_path = cookies_path
        self.autonumber_start = autonumber_start

    def run(self):
        try:
            if self.filetype == "mp4":
                cmd = [
                    "yt-dlp",
                    "--force-overwrites",
                    "--cookies", str(self.cookies_path),
                    "-f", "bv*[vcodec^=avc1]+ba[acodec^=mp4a]/mp4",
                    "--merge-output-format", "mp4",
                    "-o", self.output_path,
                ]

            elif self.filetype == "mp3":
                cmd = [
                    "yt-dlp",
                    "--cookies", str(self.cookies_path),
                    "-x", "--audio-format", "mp3",
                    "-o", self.output_path,
                ]

            else:
                raise ValueError("Invalid filetype. Choose 'mp3' or 'mp4'.")

            # Add autonumbering (applies to mp3 and mp4)
            if self.autonumber_start is not None:
                cmd.extend(["--autonumber-start", str(self.autonumber_start)])

            # URL always goes at the end
            cmd.append(self.url)

            # Run the process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                self.log.emit(line.strip())

            process.wait()
            success = process.returncode == 0
            self.done.emit(success)

        except Exception as e:
            self.log.emit(f"Error: {e}")
            self.done.emit(False)
