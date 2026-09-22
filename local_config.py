from pathlib import Path

class Config:
    def __init__(self):

        storage_folder = Path(r'C:\Users\ccole\Desktop\storage')
        self.playlist_folder = 'src\playlist_editor\playlists' # the folder with the playlist text files
        self.video_folder = str(storage_folder / 'videos') # the folder that holds videos
        self.song_folder = str(storage_folder / 'songs') # the folder that holds songs (If you have a parent songFolder with a subfolder for a group of songs like a game ost, use the parent folder.)
        self.audio_folder = str(storage_folder / 'audios') # the folder that holds audio clips
        self.image_folder = str(storage_folder / 'images') # the folder that holds images
        self.gif_folder = str(storage_folder / 'gifs') # the folder that holds gifs

        self.storage_folder = str(storage_folder)