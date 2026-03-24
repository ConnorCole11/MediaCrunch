import os

class ControlPlaylist:
    def __init__(self, playlist_path: str, songs_root: str):
        """
        playlist_path: path to the playlist .txt file
        songs_root: path to the songs/ directory
        """
        self.playlist_path = playlist_path
        self.songs_root = songs_root
        self.tracks = []  # list of relative paths like "Xenoblade/Uraya_day_theme.mp3"

        if os.path.exists(playlist_path):
            self.load()

    def load(self):
        with open(self.playlist_path, "r", encoding="utf-8") as f:
            self.tracks = [line.strip() for line in f.readlines() if line.strip()]

    def save(self):
        with open(self.playlist_path, "w", encoding="utf-8") as f:
            for track in self.tracks:
                f.write(track + "\n")

    def add_track(self, full_path: str):
        """
        full_path: full absolute path to the song file.
        Converts it to relative-from-songs/ before saving.
        """
        rel_path = os.path.relpath(full_path, self.songs_root)
        if rel_path not in self.tracks:
            self.tracks.append(rel_path)

    def remove_track(self, index: int):
        if 0 <= index < len(self.tracks):
            del self.tracks[index]

    def move_track(self, old_index: int, new_index: int):
        if 0 <= old_index < len(self.tracks):
            track = self.tracks.pop(old_index)
            self.tracks.insert(new_index, track)
