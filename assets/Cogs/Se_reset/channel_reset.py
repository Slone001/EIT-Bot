import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Context
import assets
import logging


class channel_reset(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("Basic_Logger")
        self.reset_channel: list[int] = []
        self.news_channel_id = 910640466066833438
        self.delete_channels: list[discord.TextChannel] = []

    @commands.command(name="channel_rest", aliases=["cr"])
    @commands.has_any_role("Admin")
    def reset_channels(self, ctx: Context):
        guild = ctx.guild
        channels = guild.channels
        reset_channel: list[discord.VoiceChannel] = []
        for channel in channels:
            if channel.id in self.reset_channel:
                reset_channel.append(channel)

        for channel in reset_channel:
            f = open(f"{channel.name}_{datetime.date.today().strftime('%y_%m_%d')}.txt", "r")
            self.delete_channels = [messages async for messages in channel.history(limit=99999, oldest_first=True)]
            for message in self.delete_channels:
                f.write(f"{message.author}, {message.created_at}: {message.content}\n")
            f.close()
    #todo: Channel history sends to channel



