class PlayerState:
    """
    Holds the states of the player engine (booleans, values, etc).
    """

    def __init__(self):

        # Initialize Values
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

        self.current_song = None
        self.current_song_name = None
        self.current_idx = 0
