import discord
from discord.ext import commands
from discord.ext.commands import Context
import assets
import logging



class Admin(commands.Cog):

    def __init__(self, bot: commands.Cog):
        self.bot = bot
        self.logger = logging.getLogger("Basic_Logger")
        self.admin_role = 938405640290852874

    @commands.command(name="admin", aliases=["a"])
    @commands.has_permissions(adminosttrator=True)
    async def admin(self, ctx: Context):
        message = ctx.message.content.split(" ")
        if message[2].lower == "add_default_role":
            self.add_default_role(ctx)
        elif message[2].lower == "rm_default_role":
            self.rm_default_role(ctx)

    def add_default_role(self, ctx: Context):
        pass

    def rm_default_role(self, ctx: Context):
        pass


