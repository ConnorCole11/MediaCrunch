# Player.py

from PyQt5.QtCore import QObject, pyqtSignal
from mutagen.mp3 import MP3
import pygame
import random
import time
import os


class Player(QObject):
    songChanged = pyqtSignal(int)
    pausedChanged = pyqtSignal(bool)
    shuffleChanged = pyqtSignal(bool)

    def __init__(self, playlist_file, song_folder):
        super().__init__()

        self.plist_dir = playlist_file
        self.song_folder = song_folder

        # Global Values
        self.loop = False
        self.end = False
        self.pause_song = False
        self.skip_song = False
        self.skip_n_songs = 1
        self.back_a_song = False
        self.current_idx = 0
        self.error_message = ""
        self.volume = 0.5
        self.shuffle = False

    def get_songs(self):
        with open(self.plist_dir, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        self.song_dirs = [
            os.path.join(self.song_folder, line)
            for line in lines if line.endswith(".mp3")
        ]
        return self.song_dirs
    
    def shuffle_songs(self):
        self.shuffle = not self.shuffle
        self.shuffleChanged.emit(self.shuffle)  # update UI label
        if self.shuffle:
            random.shuffle(self.song_dirs)
        else:
            self.get_songs()  # reset to original order

        self.current_idx = 0
        self.songChanged.emit(self.current_idx)  # highlight first song in new order


    @staticmethod
    def get_mp3_duration(song):
        audio = MP3(song)
        return audio.info.length

    def play_songs(self):
        song_dirs = self.song_dirs
        self.current_idx = 0
        pause_looped = False
        i = 0

        while 0 <= i < len(song_dirs) and not self.end:

            self.current_idx = i
            self.songChanged.emit(self.current_idx)   # ⭐ signal instead of callback

            mp3 = song_dirs[i]
            mp3_length = self.get_mp3_duration(mp3)

            pygame.mixer.music.load(mp3)
            time.sleep(1)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(self.volume)
            start_time = time.time()

            while (pygame.mixer.music.get_busy() or self.pause_song or self.loop) and not self.end:

                time.sleep(0.5)

                if self.skip_song:
                    self.skip_song = False
                    self.loop = False
                    self.pause_song = False
                    pygame.mixer.music.stop()
                    break

                if self.back_a_song:
                    self.back_a_song = False
                    self.pause_song = False
                    self.loop = False
                    pygame.mixer.music.stop()
                    if i == 0:
                        i = -1
                    else:
                        i -= 2
                    break

                if self.loop and not pygame.mixer.music.get_busy() and not self.pause_song:
                    pygame.mixer.music.play()

                if self.pause_song:
                    if not pause_looped:
                        pause_looped = True
                    continue
                elif pause_looped:
                    pause_looped = False

            if not self.loop:
                i += int(self.skip_n_songs)
                self.skip_n_songs = 1

    # controls unchanged
    def tog_loop(self): 
        self.loop = not self.loop

    def pause(self):
        self.pause_song = True
        self.pausedChanged.emit(True)

    def unpause(self):
        self.pause_song = False
        self.pausedChanged.emit(False)

    def skip(self): 
        self.skip_song = True

    def back(self): 
        self.back_a_song = True

    def idx(self, song_index: int): 
        self.current_idx = song_index