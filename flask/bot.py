# bot.py
from discord.ext import commands
from dotenv import load_dotenv
import random
import os
from music import Music

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
    guild = ctx.message.guild
    await music.play(guild, url)


@bot.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
async def leave(ctx):
    await music.leave(ctx.message.guild, ctx.message.channel)


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

if __name__ == '__main__':
    bot.run(TOKEN)
