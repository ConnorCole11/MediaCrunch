from pathlib import Path

class Config:
    def __init__(self):

        # recommend putting a videos, songs, audios, images, and gifs folders inside a "storage" folder
        storage_folder = Path("...") 

        self.playlist_folder = '...' # the folder with the playlist text files
        self.video_folder = storage_folder / '...' # the folder that holds videos
        self.song_folder = storage_folder / '...' # the folder that holds songs (and song folders within it)
        self.audio_folder = storage_folder / '...' # the folder that holds audio clips
        self.image_folder = storage_folder / '...' # the folder that holds images
        self.gif_folder = storage_folder / '...' # the folder that holds gifs