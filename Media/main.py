try: 
    from config_local import Config 
except ImportError: 
    from config import Config

from music.makePlaylist.main import makePlaylist_main
from music.musicPlayer.main import musicPlayer_main

config = Config()
# makePlaylist_main(config)
musicPlayer_main(config)
