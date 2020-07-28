import os


class Song:
    def __init__(self, youtube_url, file):
        self.url = youtube_url
        self.file_name = file


class SongCache:
    def __init__(self):
        self.cache: [Song] = []
        self.cache_limit = 20
        self.clear_cache()

    """
    Temporary solution that clears cache every time we start up the system as I haven't thought of a way to recreate
    all the song objects yet
    """
    @staticmethod
    def clear_cache():
        for file in os.listdir("./music_cache"):
            if file.endswith(".mp3"):
                os.remove(file)

    """
    Attempts the removal of a song and fails if it is playing. Returns true if the method was successful and False 
    otherwise
    
    :param file: File to remove
    :return bool: Whether the removal was successful
    """
    @staticmethod
    def attempt_removal(file: str) -> bool:
        try:
            os.remove(file)
            return True
        except PermissionError:
            print("Song currently playing")
            return False

    """
    Attempts to append a song to the cache and removes older songs if possible
    
    :param song: song to add
    """
    def append(self, song: Song):
        if len(self.cache) <= self.cache_limit:
            self.cache.append(song)
            return

        num_over = len(self.cache) - self.cache_limit
        for over_limit in range(num_over):
            song = self.cache.pop()
            if self.attempt_removal(song.file_name):
                continue
            self.cache.append(song)

    """
    Get a song from the cache using the url, returns None if it can't be found
    
    :param url: Youtube URL for the song
    :return song or None: Return the song if found, else None
    """
    def get_song(self, url: str) -> Song or None:
        for song in self.cache:
            if song.url == url:
                return song
        return None
