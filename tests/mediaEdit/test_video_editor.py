import os
import pytest
from unittest.mock import patch, MagicMock

from src.mediaEdit.videoEdit.video_editor import VideoEditor


# =========================
# Helpers
# =========================

class FakeClip:
    def __init__(self):
        self.w = 1920
        self.h = 1080
        self.fps = 30.0
        self.duration = 10.0
        self.audio = MagicMock()
        self.audio.fps = 44100
        self.audio.nchannels = 2

    def resize(self, width=None, height=None):
        if width:
            self.w = width
        if height:
            self.h = height
        return self

    def set_fps(self, fps):
        self.fps = fps
        return self

    def close(self):
        pass


# =========================
# Fixtures
# =========================

@pytest.fixture
def fake_mp4_file(tmp_path):
    file = tmp_path / "test.mp4"
    file.write_text("fake video content")
    return str(file)


# =========================
# INIT TESTS
# =========================

def test_init_valid_mp4(fake_mp4_file):
    with patch("src.mediaEdit.videoEdit.video_editor.VideoFileClip", return_value=FakeClip()):
        editor = VideoEditor(fake_mp4_file)
        assert editor.filepath == fake_mp4_file


def test_init_invalid_extension(tmp_path):
    bad_file = tmp_path / "test.txt"
    bad_file.write_text("not video")

    with pytest.raises(ValueError):
        VideoEditor(str(bad_file))


def test_init_missing_file():
    with pytest.raises(FileNotFoundError):
        VideoEditor("does_not_exist.mp4")


# =========================
# INFO TEST
# =========================

def test_info(fake_mp4_file):
    with patch("src.mediaEdit.videoEdit.video_editor.VideoFileClip", return_value=FakeClip()):
        editor = VideoEditor(fake_mp4_file)

        info = editor.info()

        assert info["path"] == fake_mp4_file
        assert info["resolution"] == "1920x1080"
        assert info["fps"] == 30.0
        assert info["audio_channels"] == 2


# =========================
# BITRATE TEST
# =========================

def test_get_bitrate(fake_mp4_file):
    with patch("src.mediaEdit.videoEdit.video_editor.VideoFileClip", return_value=FakeClip()):
        editor = VideoEditor(fake_mp4_file)

        fake_result = MagicMock()
        fake_result.stdout = "bit_rate=1000000\n"

        with patch("subprocess.run", return_value=fake_result):
            bitrate = editor.get_bitrate()
            assert "1000000" in bitrate


# =========================
# RESIZE TEST
# =========================

def test_resize(fake_mp4_file):
    with patch("src.mediaEdit.videoEdit.video_editor.VideoFileClip", return_value=FakeClip()):
        editor = VideoEditor(fake_mp4_file)

        editor.resize(width=1280)

        assert editor.clip.w == 1280


# =========================
# FPS TEST
# =========================

def test_change_fps(fake_mp4_file):
    with patch("src.mediaEdit.videoEdit.video_editor.VideoFileClip", return_value=FakeClip()):
        editor = VideoEditor(fake_mp4_file)

        editor.change_fps(60)

        assert editor.clip.fps == 60


# =========================
# REENCODE TEST (NO REAL FFmpeg)
# =========================

def test_reencode(fake_mp4_file):
    with patch("src.mediaEdit.videoEdit.video_editor.VideoFileClip", return_value=FakeClip()):
        editor = VideoEditor(fake_mp4_file)

        with patch("subprocess.run") as mock_run:
            output = editor.reencode(
                output_path="out.mp4",
                fps=60,
                width=1280
            )

            mock_run.assert_called_once()
            assert output == "out.mp4"


# =========================
# CLOSE TEST
# =========================

def test_close(fake_mp4_file):
    clip = FakeClip()

    with patch("src.mediaEdit.videoEdit.video_editor.VideoFileClip", return_value=clip):
        editor = VideoEditor(fake_mp4_file)
        editor.close()
