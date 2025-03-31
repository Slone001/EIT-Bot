import asyncio
import json
import discord
from discord.ext import commands
from discord.ext.commands import Context
import assets
import logging


class role_reset(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("Basic_Logger")
        # self.standard_roles: standard roles on discord-server, which shouldn't removed with command reset_ranks
        self.standard_roles: list[int]
        self.news_channel_id: int
        self.reaction_role_channel_id: int
        self.log_channel_id: int
        with open("files/data.json", "r") as f:
            data = json.load(f)
            for entry in data:
                if entry["typ"] == "default_roles":
                    self.standard_roles = entry["roles"]
                    continue
                if entry["typ"] == "admin_roles":
                    for role in entry["roles"]:
                        self.standard_roles.append(role)
                    continue
                if entry["typ"] == "news_channel":
                    self.news_channel_id = int(entry["id"])
                    continue
                if entry["typ"] == "reaction_channel":
                    self.reaction_role_channel_id = int(entry["id"])
                    continue
                if entry["typ"] == "log_channel":
                    self.log_channel_id = int(entry["id"])



    @commands.command(name="reset_ranks", aliases=["rr"])
    @commands.has_any_role("Admin")
    async def rank_reset(self, ctx: Context):
        # todo: create backup log file for old roles
        guild = ctx.guild
        guild_member = guild.members
        guild_roles = guild.roles
        print(self.standard_roles)
        remove_roles = [i for i in guild_roles if i.id not in self.standard_roles]
        del remove_roles[0]
        print(remove_roles)
        for member in guild_member:
            if not member.bot:
                print(member)
                user_remove_roles = []
                for role in member.roles:
                    if role in remove_roles:
                        user_remove_roles.append(role)
                print(user_remove_roles)
                await member.remove_roles(*user_remove_roles)
                await asyncio.sleep(1)

        news_channel = self.bot.get_channel(self.news_channel_id)
        rr_chanel = self.bot.get_channel(self.reaction_role_channel_id)
        log_channel = self.bot.get_channel(self.log_channel_id)
        await news_channel.send(f"Die Semester-Rollen wurden zurückgesetzt. Bitte weise dir die Passenden Rollen in "
                                f"dem Channel {rr_chanel.mention} ab")
        await log_channel.send(f"Die Semester-Rollen wurden von {ctx.author.name} zurückgesetzt.")


async def role_reset_setup(bot):
    """ Setup role-reset """
    await bot.add_cog(role_reset(bot))
    logging.getLogger("Basic_Logger").info(f"initialisation role-reset finished")