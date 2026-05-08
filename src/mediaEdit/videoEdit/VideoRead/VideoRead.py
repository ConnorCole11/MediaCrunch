import subprocess
import json
import os

class VideoInfo:
    def __init__(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} does not exist")
        self.filepath = filepath

    def _get_ffprobe_info(self):
        """Run ffprobe to get video information in JSON format"""
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            self.filepath
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return json.loads(result.stdout)

    def _parse_info(self):
        self.format_info = self.info.get('format', {})
        self.streams = self.info.get('streams', [])

        # General info
        self.filesize = int(self.format_info.get('size', 0))
        self.duration = float(self.format_info.get('duration', 0))
        self.bitrate = int(self.format_info.get('bit_rate', 0)) if 'bit_rate' in self.format_info else None

        # Separate streams
        self.video_stream = next((s for s in self.streams if s['codec_type'] == 'video'), None)
        self.audio_stream = next((s for s in self.streams if s['codec_type'] == 'audio'), None)

        # Video info
        if self.video_stream:
            self.width = int(self.video_stream.get('width', 0))
            self.height = int(self.video_stream.get('height', 0))
            self.fps = self._parse_fps(self.video_stream.get('r_frame_rate', '0/0'))
            self.video_bitrate = int(self.video_stream.get('bit_rate', 0)) if 'bit_rate' in self.video_stream else None

        # Audio info
        if self.audio_stream:
            self.audio_bitrate = int(self.audio_stream.get('bit_rate', 0)) if 'bit_rate' in self.audio_stream else None
            self.audio_channels = int(self.audio_stream.get('channels', 0))
            self.audio_sample_rate = int(self.audio_stream.get('sample_rate', 0))

        # Estimate audio/video size separately if bitrates exist
        if self.video_bitrate and self.audio_bitrate:
            self.video_size = int((self.video_bitrate / 8) * self.duration)
            self.audio_size = int((self.audio_bitrate / 8) * self.duration)
        else:
            self.video_size = None
            self.audio_size = None

    @staticmethod
    def _parse_fps(fps_str):
        try:
            num, denom = fps_str.split('/')
            return float(num) / float(denom)
        except:
            return 0.0

    def summary(self, human_readable=True):
        """Return summary info. If human_readable, converts bytes to MB."""
        def to_mb(x):
            return round(x / (1024 * 1024), 2) if x else None

        summary = {
            'filepath': self.filepath,
            'filesize_bytes': self.filesize,
            'duration_sec': self.duration,
            'overall_bitrate_bps': self.bitrate,
            'video': {
                'width': getattr(self, 'width', None),
                'height': getattr(self, 'height', None),
                'fps': getattr(self, 'fps', None),
                'bitrate_bps': getattr(self, 'video_bitrate', None),
                'size_bytes': getattr(self, 'video_size', None)
            },
            'audio': {
                'channels': getattr(self, 'audio_channels', None),
                'sample_rate': getattr(self, 'audio_sample_rate', None),
                'bitrate_bps': getattr(self, 'audio_bitrate', None),
                'size_bytes': getattr(self, 'audio_size', None)
            }
        }

        if human_readable:
            summary['filesize_MB'] = to_mb(self.filesize)
            if self.video_size:
                summary['video']['size_MB'] = to_mb(self.video_size)
            if self.audio_size:
                summary['audio']['size_MB'] = to_mb(self.audio_size)

        return summary

