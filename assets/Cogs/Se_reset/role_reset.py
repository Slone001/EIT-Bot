import asyncio
import json
from discord.ext import commands
from discord.ext.commands import Context
import assets
import logging
import datetime


class role_reset(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("Basic_Logger")
        self.standard_roles: list[int]
        self.news_channel_id: int
        self.reaction_role_channel_id: list[int]
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
                    self.reaction_role_channel_id = entry["id"]
                    continue
                if entry["typ"] == "log_channel":
                    self.log_channel_id = int(entry["id"])

    @commands.command(name="reset_ranks", aliases=["rr"])
    @commands.has_any_role("Admin")
    async def rank_reset(self, ctx: Context):
        self.logger.info(f"Role reset activated by {ctx.author}")
        await ctx.channel.send(f"Role reset activated by {ctx.author.name}")
        guild = ctx.guild
        guild_member = guild.members
        guild_roles = guild.roles
        remove_roles = [i for i in guild_roles if i.id not in self.standard_roles]
        filename = f"role_reset_{datetime.datetime.now().strftime('%Y_%m_%d %H,%M,%S')}.csv"
        file = open(f"{assets.Logs}{filename}", "a")
        del remove_roles[0]
        for member in guild_member:
            if not member.bot:
                user_remove_roles = []
                for role in member.roles:
                    if role in remove_roles:
                        user_remove_roles.append(role)
                        file.write(f"{member.name}, {member.id}, {role.name}, {role.id}\n")
                await member.remove_roles(*user_remove_roles)
                await asyncio.sleep(1)

        file.close()
        news_channel = self.bot.get_channel(self.news_channel_id)
        log_channel = self.bot.get_channel(self.log_channel_id)
        channels: str = ""
        for channel_id in self.reaction_role_channel_id:
            rr_chanel = self.bot.get_channel(channel_id)
            if channels == "":
                channels += f"{rr_chanel.mention}"
            else:
                channels += f", {rr_chanel.mention}"
        await news_channel.send(f"Die Semester-Rollen wurden zurückgesetzt. Bitte weise dir die passenden Rollen für "
                                f"das kommende Semester in den Kanälen {channels} zu")
        await log_channel.send(f"Die Semester-Rollen wurden von {ctx.author.name} zurückgesetzt.")
        self.logger.info("Role reset finished")


async def role_reset_setup(bot):
    """ Setup role-reset """
    await bot.add_cog(role_reset(bot))
    logging.getLogger("Basic_Logger").info(f"initialisation role-reset finished")