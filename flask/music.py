from discord.utils import get
import os
import discord
import youtube_dl
from song_cache import Song, SongCache
import asyncio
import threading
import time


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.song_cache: SongCache = SongCache()
        self.player_queue: dict = dict()

    class Player:
        def __init__(self, guild):
            self.guild = guild
            self.playing: bool = False
            self.queue: [Song] = []
            self.thread: threading.Thread or None = None

        """
        Adds a song to the queue and then starts the player thread
        """
        def add_queue(self, song: Song):
            self.queue.append(song)
            if self.thread is not None and self.thread.is_alive():
                return
            self.playing = True
            self.thread = threading.Thread(target=self.starts, args=(lambda: self.playing,))
            self.thread.start()

        """
        Pops the first element out of the queue and returns it
        """
        def dequeue(self) -> Song or None:
            if len(self.queue) == 0:
                return None
            return self.queue.pop(0)

        """
        Player thread to run in order to continuously run song in the queue, iteratively
        """
        def starts(self, playing):
            while playing():
                if self.guild.voice_client.is_playing():
                    continue

                song = self.dequeue()
                if song is None:
                    break
                self.play_file(song.file_name)
                time.sleep(1)

        """
        Stops the player and then stops the voice client
        """
        def stop(self):
            self.playing = False
            self.guild.voice_client.stop()
            #todo: discuss deleting queue on stop

        """
        This will stop the player from playing, so that it doesn't play the next song in the queue and then it will 
        pause the audio file
        """
        def pause(self):
            self.playing = False
            self.guild.voice_client.pause()

        """
        Resume also needs to start back up the player, assuming that the pause method was called
        """
        def resume(self):
            self.playing = True
            voice = self.guild.voice_client
            voice.resume()
            self.thread = threading.Thread(target=self.starts, args=(lambda: self.playing,))
            self.thread.start()

        """
        If player is playing, this command will just stop the voice client to queue and play the next song
        """
        def skip(self):
            self.guild.voice_client.stop()

        """
        Plays the specified file in the guild's voice client

        :param guild: guild to play music in
        :param file: file to play
        """
        def play_file(self, file):
            voice = self.guild.voice_client
            voice.play(discord.FFmpegPCMAudio(file))
            voice.volume = 100
            voice.is_playing()

    """
    Downloads a song based on a url from youtube. It will also cache the downloaded file.
    
    :param youtube_url: URL to youtube video
    """
    def download_song(self, youtube_url) -> Song:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    file_location = f'./music_cache/{file}'
                    os.rename(file, file_location)
                    song = Song(youtube_url, file_location)
                    self.song_cache.append(song)
                    return song

    @staticmethod
    def get_default_text_channel(guild) -> discord.TextChannel:
        channel = get(guild.channels, name='bots')
        return channel

    """
    Gets the song from the specified url and returns the associated object to be used. It takes as parameter as a
    coroutine that gets executed to give feedback that there will be a download and this will delay the playing of the
    song.
    """
    async def get_song(self, youtube_url: str, dl_delay_msg=asyncio.coroutine(lambda: print("Song not in cache"))) -> \
            Song:
        song = self.song_cache.get_song(youtube_url)
        if song is None:
            await dl_delay_msg()
            song = self.download_song(youtube_url)
        return song

    """
    This method is for having the bot join a specific channel. If a channel is specified, it will send a confirmation
    message on join
    
    :param guild: is for the server
    :param voice_channel: for the voice channel to join in the server
    :param channel: for the text channel to send the message to
    """
    async def join_channel(self, guild, voice_channel, channel=None):
        voice = get(self.bot.voice_clients, guild=guild)
        if voice and voice.is_connected():
            await voice.move_to(voice_channel)
        else:
            voice = await voice_channel.connect()
        if channel is None:
            channel = self.get_default_text_channel(guild)
        await channel.send(f"Joined {voice_channel}")

    """
    Given that the bot is connected to a voice channel at the specified guild, play the audio at the specified 
    youtube url
    
    :param guild: The server that you want the audio to start playing in
    :param youtube_url: The youtube url that you would like to start playing
    """
    async def play(self, guild, youtube_url, channel=None):
        print("Someone wants to play music let me get that ready for them...")

        if channel is None:
            channel = self.get_default_text_channel(guild)
        song = await self.get_song(youtube_url, lambda: channel.send("Getting everything ready, playing audio soon"))
        self.player_queue[guild.name].play_file(song.file_name)

    """
    Pauses the audio that is playing in a guild
    
    :param guild: guild to pause audio for
    """
    async def pause(self, guild):
        print("Pausing Audio")
        self.player_queue[guild.name].pause()

    """
    Resumes whatever was playing at the time the audio was paused
    
    :param guild: guild to resume audio for
    """
    async def resume(self, guild):
        print("Resuming Audio")
        self.player_queue[guild.name].resume()

    """
    Stops song/audio file and removes it
    
    :param guild: guild to stop audio for
    """
    async def stop(self, guild):
        print("Stopping Audio")
        self.player_queue[guild.name].stop()

    """
    Skips to the next song/audio file and plays it
    
    :param guild: guild to skip to the next song for
    """
    async def skip(self, guild):
        print("Skipping Song")
        self.player_queue[guild.name].skip()

    """
    Leaves a voice chat if the bot is in one in the specified guild
    
    :param guild: The server for which you would like the bot to leave the voice chat in
    :param channel: The channel for which you want the feedback messages to be sent
    """
    async def leave(self, guild, channel=None):
        voice = get(self.bot.voice_clients, guild=guild)
        if channel is None:
            channel = self.get_default_text_channel(guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            await channel.send(f"Left {voice.channel}")
        else:
            await channel.send("Don't think I am in a voice channel")

    async def queue(self, guild, url):
        print("Queuing Song")
        song = await self.get_song(url)
        self.player_queue[guild.name].add_queue(song)
