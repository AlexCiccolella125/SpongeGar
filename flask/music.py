from discord.utils import get


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

