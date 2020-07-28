from discord.utils import get
import os
import discord
import youtube_dl
from song_cache import Song, SongCache


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.song_cache: SongCache = SongCache()

    """
    Plays the specified file in the guild's voice client
    
    :param guild: guild to play music in
    :param file: file to play
    """
    @staticmethod
    def play_file(guild, file):
        voice = guild.voice_client
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
        song = self.song_cache.get_song(youtube_url)
        if song is None:
            await channel.send("Getting everything ready, playing audio soon")
            song = self.download_song(youtube_url)
        self.play_file(guild, song.file_name)


    """
    Pauses the audio that is playing in a guild
    
    :param guild: guild to pause audio for
    """
    async def pause(self, guild):
        print("Pausing Audio")
        voice = guild.voice_client
        voice.pause()

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
