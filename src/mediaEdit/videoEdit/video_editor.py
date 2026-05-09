import os
import subprocess
from moviepy import VideoFileClip

class VideoEditor:
    """
    Video editing and encoding control for properly formatted MP4 files.
    Assumes video uses H.264 + AAC codecs.
    """

    def __init__(self, filepath: str):
        if not os.path.exists(filepath):
            raise FileNotFoundError(filepath)

        if not filepath.lower().endswith(".mp4"):
            raise ValueError("VideoEditor only accepts .mp4 files.")

        self.filepath = filepath
        self.clip = VideoFileClip(filepath)
        print(f"Loaded {filepath} ({self.clip.w}x{self.clip.h} @ {self.clip.fps:.2f}fps)")

    # ===============
    # INFO / METADATA
    # ===============

    def info(self):
        """Return basic video metadata."""
        return {
            "path": self.filepath,
            "duration": self.clip.duration,
            "resolution": f"{self.clip.w}x{self.clip.h}",
            "fps": self.clip.fps,
            "audio_fps": getattr(self.clip.audio, 'fps', None),
            "audio_channels": getattr(self.clip.audio, 'nchannels', None)
        }

    def get_bitrate(self) -> str:
        """Return approximate bitrate via ffprobe."""
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=bit_rate", "-of", "default=nw=1", self.filepath],
                capture_output=True, text=True
            )
            return result.stdout.strip() or "unknown"
        except Exception:
            return "unknown"

    # =============
    # OPERATIONS
    # =============

    def resize(self, width: int = None, height: int = None):
        """Resize video; preserves aspect ratio if only one dimension given."""
        self.clip = self.clip.resize(width=width, height=height)
        print(f"Resized to {self.clip.w}x{self.clip.h}")
        return self

    def change_fps(self, new_fps: float):
        """Change playback frame rate (can increase or decrease)."""
        self.clip = self.clip.set_fps(new_fps)
        print(f"Changed FPS to {new_fps}")
        return self

    def reencode(self, output_path="reencoded.mp4", bitrate="2M", fps=None, width=None, height=None, preset="medium"):
        """
        Re-encode the video with new bitrate, resolution, or FPS.
        Useful for upscaling, downscaling, or size optimization.
        """
        cmd = [
            "ffmpeg", "-y",
            "-i", self.filepath,
            "-c:v", "libx264",
            "-preset", preset,
            "-c:a", "aac",
            "-b:v", bitrate,
            "-movflags", "+faststart"
        ]

        if fps:
            cmd += ["-r", str(fps)]
        if width or height:
            scale_expr = f"scale={width or -1}:{height or -1}"
            cmd += ["-vf", scale_expr]

        cmd.append(output_path)
        subprocess.run(cmd, check=True)
        print(f"Re-encoded video saved → {output_path}")
        return output_path

    # =================
    # Cleanup 
    # =================

    def close(self):
        """Release resources."""
        self.clip.close()


