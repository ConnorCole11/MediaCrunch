from mutagen.mp3 import MP3
from cc_files import gen
import pygame
import time
import os

class Player:
    def __init__(self, playlist_dir, song_folder, on_song_change=None):
        self.plist_dir = playlist_dir
        self.song_folder = song_folder

        # Global Values
        self.loop = False # Loop song
        self.end = False # Quits code
        self.pause_song = False # Pauses
        self.skip_song = False # Skip song
        self.skip_n_songs = 1 # Skip n songs (argument for skip)
        self.back_a_song = False # Go back a song
        self.current_idx = 0 # Current song idx playing
        self.error_message = ""

        self.volume = 0.5  # default 50%
        self.on_song_change = on_song_change   # callback function for gui


    # ===============
    # Song Management
    # ===============

    def get_songs(self): 
        """Takes the playlist textfile directory and returns the song directories."""
        with open(self.plist_dir, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        song_dirs = [os.path.join(self.song_folder, line) for line in lines if line.endswith(".mp3")]
        self.song_dirs = song_dirs
        return self.song_dirs

    @staticmethod
    def get_mp3_duration(song):
        """Take specific mp3 file and return the length of the file, in seconds."""
        audio = MP3(song)
        return audio.info.length  # in seconds
    

    # Plays songs from the list of song filenames, and controls effects of skips, backs, pause,loops, etc.
    def play_songs(self):
        """Play songs """
        song_dirs = self.song_dirs
        self.current_idx = 0
        pause_looped = False
        i = 0
        while 0 <= i < len(song_dirs) and not self.end:
            # Define constants
            self.current_idx = i  # Update current index to match current song
            if self.on_song_change:
                try:
                    self.on_song_change(self.current_idx)  # call GUI callback immediately
                except Exception:
                    pass
            mp3 = song_dirs[i] # Grab current song
            # print(f"Current song path: {mp3}")
            mp3_length = self.get_mp3_duration(mp3) # Length of current song
            # print(f"Playing: {mp3}...")
            pygame.mixer.music.load(mp3)
            time.sleep(1)  # Small delay before playing 
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(self.volume)
            start_time = time.time()

            while (pygame.mixer.music.get_busy() or self.pause_song or self.loop) and not self.end:

                time.sleep(0.5)
                current_time = time.time() - start_time
                # run_ui(mp3, mp3_length, glob.global_array, glob.error_message, glob.pause_song)

                # Handle skipping songs
                if self.skip_song:
                    self.skip_song = False
                    self.loop = False
                    self.pause_song = False

                    pygame.mixer.music.stop()
                    break  # Exit inner while to advance index

                # Handle going back
                if self.back_a_song:
                    self.back_a_song = False
                    self.pause_song = False
                    self.loop = False

                    pygame.mixer.music.stop()
                    if i == 0:
                        i = -1  # So after increment it becomes 0 again (no previous songs to current one)
                    else:
                        i -= 2  # Because we'll add 1 later, so -2 goes back one song
                    break  # Exit inner while to update index

                # Loop current song only if not paused and song ended
                if self.loop and not pygame.mixer.music.get_busy() and not self.pause_song:
                    pygame.mixer.music.play()

                # If paused, just wait here, skip other commands
                if self.pause_song:
                    # Paused in input function rather than here
                    if not pause_looped:
                        pause_looped = True
                        pause_time = time.time()
                    continue
                elif pause_looped: # Runs when it's not paused and it's the first time through unpaused
                    pause_looped = False
                
            # After inner loop ends (song ended or skip/back/stoplayback)
            if not self.loop:
                i += int(self.skip_n_songs)
                self.skip_n_songs = 1  # Reset


    def tog_loop(self):
        self.loop = not self.loop

    def pause(self):
        self.pause_song = True
    
    def unpause(self):
        self.pause_song = False

    def skip(self):
        self.skip_song = True
    
    def back(self):
        self.back_a_song = True
    
    def idx(self, song_index: int):
        self.current_idx = song_index



