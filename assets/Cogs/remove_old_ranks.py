import discord
from discord.ext import commands
from discord.ext.commands import Context
import assets
import logging


class rank_update(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("Basic_Logger")
        # self.standard_roles: standard roles on discord-server, which shouldn't removed with command reset_ranks
        self.standard_roles = [1087848965116014653, 1087848991804367000, 1151979461324054590]
        self.news_channel_id = 910640466066833438
        self.reaction_role_channel_id = 1227687366920114176

    @commands.command(name="reset_ranks", aliases=["rr"])
    @commands.has_any_role(assets.permission_roles)
    async def rank_reset(self, ctx: Context):
        guild = ctx.guild
        guild_member = guild.members
        guild_roles = guild.roles
        remove_roles = [i for i in guild_roles if i not in self.standard_roles]
        for member in guild_member:
            user_remove_roles = []
            for role in member.roles:
                if role in remove_roles:
                    user_remove_roles.append(role)

            await member.remove_roles(*user_remove_roles)
        news_channel = self.bot.get_channel(self.news_channel_id)
        rr_chanel = self.bot.get_channel(self.reaction_role_channel_id)
        await news_channel.send(f"Die Semester-Rollen wurden zurückgesetzt. Bitte weise dir die Passenden Rollen in "
                                f"dem Channel {rr_chanel.mention} ab")



