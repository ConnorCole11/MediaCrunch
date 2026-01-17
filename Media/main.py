try: 
    from config_local import * 
except ImportError: 
    from config import *

from music.makePlaylist.main import makePlaylist_main

makePlaylist_main()
