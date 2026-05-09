# Player.py

from PyQt5.QtCore import QObject, pyqtSignal
from mutagen.mp3 import MP3
import pygame
import random
import time
import os
from src.music_player.player.player_state import PlayerState
from pathlib import Path

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

    def _initialize_currentSong(self, song_dirs):
        self.ps.current_song = song_dirs[0]

    def _update_currentIndex(self):
        self.ps.current_idx = self.song_dirs.index(self.ps.current_song)

    def get_songs(self):
        """Sets self.song_dirs to be a list of the filenames in the song folder. Only called once."""
        with open(self.plist_dir, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        song_dirs = [
            os.path.join(self.song_folder, line)
            for line in lines if line.endswith(".mp3")
        ]
        self.normal_song_dirs = song_dirs.copy()
        self.song_dirs = song_dirs.copy()

        self._initialize_currentSong(song_dirs)

    
    def _shuffle_songs(self):
        random.shuffle(self.song_dirs)
        self._update_currentIndex()

    def _unshuffle_songs(self):
        self.song_dirs = self.normal_song_dirs.copy()
        self._update_currentIndex()

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
        Returns updated index, pause_looped flag, and whether an action occurred.
        """

        # Jump to a song that was double-clicked or restarted
        if self.ps.jump_to_index is not None:
            i = self.ps.jump_to_index
            self.ps.jump_to_index = None
            pygame.mixer.music.stop()
            return i, pause_looped, True

        # Normal skip
        if self.ps.skip_song:
            skip_amount = self.ps.skip_n_songs if self.ps.skip_n_songs != 0 else 1
            self.ps.skip_song = False
            self.ps.loop = False
            self.ps.pause_song = False
            pygame.mixer.music.stop()
            self.ps.skip_n_songs = 1
            return i + skip_amount, pause_looped, True

        # Back a song
        if self.ps.back_a_song:
            self.ps.back_a_song = False
            self.ps.pause_song = False
            self.ps.loop = False
            pygame.mixer.music.stop()
            i = i - 1 if i > 0 else 0
            return i, pause_looped, True

        # Loop
        if self.ps.loop and not pygame.mixer.music.get_busy() and not self.ps.pause_song:
            pygame.mixer.music.play()

        # Pause
        if self.ps.pause_song:
            pause_looped = True
        elif pause_looped:
            pause_looped = False

        return i, pause_looped, False


    def play_songs(self):
        self.ps.current_idx = 0
        pause_looped = False

        while 0 <= self.ps.current_idx < len(self.song_dirs) and not self.ps.end:
            self.ps.current_song = self.song_dirs[self.ps.current_idx]
            self.songChanged.emit(self.ps.current_idx)

            self._play_song(self.song_dirs[self.ps.current_idx])

            while (pygame.mixer.music.get_busy() or self.ps.pause_song or self.ps.loop) and not self.ps.end:
                time.sleep(0.5)
                new_i, pause_looped, action_taken = self._handle_playback_controls(
                    self.ps.current_idx, pause_looped
                )

                if action_taken:
                    self.ps.current_idx = new_i
                    break

            else:
                # Only increment if no skip/back/jump happened
                if not self.ps.loop:
                    self.ps.current_idx += 1

    def jump_to_song(self, song_path: str):
        index = self.song_dirs.index(song_path)

        self.ps.jump_to_index = index
        self.ps.pause_song = False
        self.ps.loop = False

    # controls unchanged
    def tog_loop(self): 
        self.ps.loop = not self.ps.loop

    def pause(self):
        self.ps.pause_song = True

    def unpause(self):
        self.ps.pause_song = False

    def skip(self):
        self.ps.skip_song = True
        self.ps.pause_song = False
        self.ps.loop = False
        pygame.mixer.music.unpause()

    def back(self):
        self.ps.back_a_song = True
        self.ps.pause_song = False
        self.ps.loop = False
        pygame.mixer.music.unpause()

    def restart(self):
        self.ps.jump_to_index = self.ps.current_idx
        self.ps.pause_song = False
        self.ps.loop = False

    def set_volume(self, volume):
        self.ps.volume = volume
        pygame.mixer.music.set_volume(volume)

    def idx(self, song_index: int): 
        self.ps.current_idx = song_index