# Player.py

from PyQt5.QtCore import QObject, pyqtSignal
from mutagen.mp3 import MP3
import pygame
import random
import time
import os
from src.musicPlayer.Player.PlayerState import PlayerState

class Player(QObject):
    """
    Controls the logic of the state of the music player.
    """
    # Signals being sent:
    songChanged = pyqtSignal(int)
    # pausedChanged = pyqtSignal(bool)
    # shuffleChanged = pyqtSignal(bool)

    def __init__(self, playlist_file, song_folder):
        super().__init__()
        self.plist_dir = playlist_file
        self.song_folder = song_folder

        # centralized state
        self.ps = PlayerState()

    def get_songs(self):
        """Sets self.song_dirs to be a list of the filenames in the song folder."""
        with open(self.plist_dir, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        song_dirs = [
            os.path.join(self.song_folder, line)
            for line in lines if line.endswith(".mp3")
        ]
        self.normal_song_dirs = song_dirs.copy()
        self.song_dirs = song_dirs.copy()
    
    def _shuffle_songs(self):
        current_song = self.ps.current_song
        random.shuffle(self.song_dirs)
        self.ps.current_idx = self.song_dirs.index(current_song)

    def _unshuffle_songs(self):
        current_song = self.ps.current_song
        self.song_dirs = self.normal_song_dirs.copy()
        self.ps.current_idx = self.song_dirs.index(current_song)

    def change_shuffle(self):
        self.ps.shuffle = not self.ps.shuffle

        if self.ps.shuffle:
            self._shuffle_songs()
        else:
            self._unshuffle_songs()

    @staticmethod
    def get_mp3_duration(song):
        """Get the length of the mp3 file."""
        audio = MP3(song)
        return audio.info.length

    def _play_song(self, mp3):
        """Load and play a single song."""
        pygame.mixer.music.load(mp3)
        time.sleep(1)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(self.ps.volume)

    def _handle_playback_controls(self, i, pause_looped):
        """
        Handles skip, back, pause, and loop logic.
        Returns updated index and pause_looped flag.
        """
        # Normal skip
        if self.ps.skip_song:
            skip_amount = self.ps.skip_n_songs if self.ps.skip_n_songs != 0 else 1
            self.ps.skip_song = False
            self.ps.loop = False
            self.ps.pause_song = False
            pygame.mixer.music.stop()
            self.ps.skip_n_songs = 1
            return i + skip_amount, pause_looped

        # Back a song
        if self.ps.back_a_song:
            self.ps.back_a_song = False
            self.ps.pause_song = False
            self.ps.loop = False
            pygame.mixer.music.stop()
            i = i - 1 if i > 0 else 0
            return i, pause_looped

        # Loop
        if self.ps.loop and not pygame.mixer.music.get_busy() and not self.ps.pause_song:
            pygame.mixer.music.play()

        # Pause
        if self.ps.pause_song:
            pause_looped = True
        elif pause_looped:
            pause_looped = False

        return i, pause_looped

    def play_songs(self):
        song_dirs = self.song_dirs
        self.ps.current_idx = 0
        pause_looped = False
        i = 0

        while 0 <= i < len(song_dirs) and not self.ps.end:
            self.ps.current_idx = i
            # self.ps.current_song = song_dirs[i]
            self.songChanged.emit(self.ps.current_idx)

            self._play_song(song_dirs[i])

            while (pygame.mixer.music.get_busy() or self.ps.pause_song or self.ps.loop) and not self.ps.end:
                time.sleep(0.5)
                new_i, pause_looped = self._handle_playback_controls(i, pause_looped)
                if new_i != i:
                    i = new_i
                    break

            else:
                # Only increment if no skip/back/jump happened
                if not self.ps.loop:
                    i += 1

    def jump_to_song(self, index: int):
        diff = index - self.ps.current_idx
        self.ps.skip_n_songs = diff
        self.ps.pause_song = False
        self.ps.loop = False
        self.ps.skip_song = True
        self.ps.current_song = self.song_dirs[index]
        pygame.mixer.music.unpause()


    # controls unchanged
    def tog_loop(self): 
        self.ps.loop = not self.ps.loop

    def pause(self):
        self.ps.pause_song = True

    def unpause(self):
        self.ps.pause_song = False

    def skip(self): 
        self.ps.skip_song = True

    def back(self): 
        self.ps.back_a_song = True

    def idx(self, song_index: int): 
        self.ps.current_idx = song_index