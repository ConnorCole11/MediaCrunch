import os
import subprocess
from moviepy import VideoFileClip

class MP4matter:
    def __init__(self, filedir: str):
        if not os.path.exists(filedir):
            raise FileNotFoundError(filedir)

        self.original_path = filedir
        self.filedir = self._ensure_mp4(filedir)

        self.clip = VideoFileClip(self.filedir)
        print(f"Loaded video: {self.filedir} ({self.clip.duration:.2f}s)")

    def _ensure_mp4(self, filedir: str) -> str:
        """
        Convert file to MP4 (H.264 + AAC) if not already safe.
        Returns path to converted file.
        """
        # Quick check
        if filedir.lower().endswith(".mp4") and self._is_h264_aac(filedir):
            return filedir

        safe_path = os.path.splitext(filedir)[0] + "_safe.mp4"
        print(f"Converting {filedir} → {safe_path}")

        # ffmpeg conversion
        cmd = [
            "ffmpeg", "-y",
            "-i", filedir,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-movflags", "+faststart",
            safe_path
        ]
        subprocess.run(cmd, check=True)
        return safe_path

    def _is_h264_aac(self, filedir: str) -> bool:
        """Use ffprobe to check if codecs are H.264 + AAC."""
        try:
            import json
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=codec_name", "-of", "json", filedir],
                capture_output=True, text=True
            )
            video_codec = json.loads(result.stdout)["streams"][0]["codec_name"]

            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "a:0",
                 "-show_entries", "stream=codec_name", "-of", "json", filedir],
                capture_output=True, text=True
            )
            audio_codec = json.loads(result.stdout)["streams"][0]["codec_name"]

            return video_codec == "h264" and audio_codec == "aac"
        except Exception:
            return False
