try: 
    from config_local import Config 
except ImportError: 
    from config import Config

from music.makePlaylist.main import makePlaylist_main
from music.musicPlayer.main import musicPlayer_main
from ytDownload.main import ytDownload_main
# mediaEdit is not yet implemented

config = Config()
# makePlaylist_main(config)
# musicPlayer_main(config)
ytDownload_main()