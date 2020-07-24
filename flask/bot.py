# bot.py
import os

from discord.ext import commands
from dotenv import load_dotenv
import random
import youtube_dl

import discord
import os
from discord.utils import get
from discord import FFmpegPCMAudio
from music import Music
from discord import TextChannel

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
music = Music(bot)



@bot.event
async def on_ready():

    print(
        f'{bot.user.name} is connected to the following guild:\n'
    )


@bot.command(name='99')
async def on_message(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

    

@bot.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    await music.join_channel(ctx.guild, channel, ctx.message.channel)

    
@bot.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music end or use the 'stop' command")
        return
    await ctx.send("Getting everything ready, playing audio soon")
    print("Someone wants to play music let me get that ready for them...")
    voice = ctx.message.guild.voice_client
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()


@bot.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
async def leave(ctx):

    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Don't think I am in a voice channel")


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

if __name__ == '__main__':
    print(TOKEN)
    bot.run(TOKEN)
