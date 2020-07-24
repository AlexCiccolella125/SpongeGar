from discord.utils import get
import os
from discord import FFmpegPCMAudio
import discord
import youtube_dl


class Music:
    def __init__(self, bot):
        self.bot = bot

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
        await voice.disconnect()
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await voice_channel.connect()
        if channel is None:
            channel = get(guild.channels, name='bots')
        await channel.send(f"Joined {voice_channel}")

    """
    Given that the bot is connected to a voice channel at the specified guild, play the audio at the specified 
    youtube url
    
    :param guild: The server that you want the audio to start playing in
    :param youtube_url: The youtube url that you would like to start playing
    """
    async def play(self, guild, youtube_url):
        print("Someone wants to play music let me get that ready for them...")
        voice = guild.voice_client
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
                os.rename(file, 'song.mp3')
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        voice.volume = 100
        voice.is_playing()

