import asyncio
import json
import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get
import assets
import logging
import datetime
import urllib.request
import sys

""" Role and channel creation with a csv as input method. Creates Roles and channel and saves them in a .json """


class csv(commands.Cog):
    """ Modulnummer,Modulname """

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('Basic_Logger')
        if sys.platform == "win32":
            self.wp_categories = 909409639039393814
        elif sys.platform == "linux":
            self.wp_categories = 1162441125202772018

    @commands.command(name="csv")
    @commands.has_any_role("Admin")
    async def csv(self, ctx: Context):
        guild = ctx.guild
        # data: list[dict] = [{"role": "502", "name": "test", "role_id": 5546454541, "channel_id": 7441454}]
        data: list[dict] = []
        attachment_url = ctx.message.attachments[0].url
        urllib.request.urlretrieve(attachment_url, f"{assets.files}csv.csv")
        with open(f"{assets.files}csv.csv", "r") as file:
            for line in file:
                line = line.split()
                if not line[0] in guild.roles:
                    role = await guild.create_role(name=line[0], reason="Wahlpflicht-modul")
                else:
                    role = get(guild.roles, name=line[0])
                if line[1] not in guild.channels:
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(view_channel=False),
                        role: discord.PermissionOverwrite(view_channel=True)
                    }
                    channel = await guild.create_text_channel(
                        name=line[1], category=get(guild.categories, id=self.wp_categories), reason="Wahlpflicht-modul",
                        overwrites=overwrites)
                else:
                    channel = get(guild.channels, name=line[1])
                data.append({"role": line[0], "name": line[1], "role_id": role.id, "channel_id": channel.id})
        with open(f"{assets.files}role_data.json", "r") as file:
            new_data: list[dict] = json.load(file)
        new_data += data
        with open(f"{assets.files}role_data.json", "w") as file:
            file.write(json.dumps(new_data, indent=4))


