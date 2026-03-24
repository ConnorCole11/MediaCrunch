# Enter absolute paths to:
from pathlib import Path
class Config:
    def __init__(self):
        mediaCrunch_path = Path('/Users') / 'ColeFamily/Desktop/MediaCrunch'

        self.playlist_folder = mediaCrunch_path / 'src/playlistEditor/playlists' # the folder with the playlist text files
        self.video_folder = mediaCrunch_path / 'storage/videos' # the folder that holds videos
        self.song_folder = mediaCrunch_path / 'storage/songs' # the folder that holds songs (If you have a parent songFolder with a subfolder for a group of songs like a game ost, use the parent folder.)
        self.audio_folder = mediaCrunch_path / 'storage/audios' # the folder that holds audio clips
        self.image_folder = mediaCrunch_path / 'storage/images' # the folder that holds images
        self.gif_folder = mediaCrunch_path / 'storage/gifs' # the folder that holds gifs