try: 
    from config_local import Config 
except ImportError: 
    from config import Config

from music.makePlaylist.main import makePlaylist_main

config = Config()
makePlaylist_main(config)
