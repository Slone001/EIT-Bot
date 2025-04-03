import asyncio
import json
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
    # @commands.has_any_role("Admin", "Moderator")
    @commands.is_owner()
    async def admin(self, ctx: Context):
        message = ctx.message.content.split(" ")
        if message[2].lower == "add_default_role" or "adr":
            await self.add_default_role(ctx)
        elif message[2].lower == "rm_default_role" or "rdr":
            self.rm_default_role(ctx)

    async def add_default_role(self, ctx: Context):
        message = ctx.message.content.split(" ")
        try:
            role = discord.utils.get(ctx.guild.roles, id=(int((message[3])[3:-1])))
        except Exception:
            return
        with open(f"{assets.files}{assets.data}", mode="r+") as f:
            try:
                file = f.read()
                print("File ", file)
                i: dict
                for i in file:
                    print(i)
                    if i["typ"] == "default_roles":
                        roles: list = i["roles"]
                        new = {"name": role.name, "id": role.id}
                        roles.append(new)
                        file.update(roles)
                        print(1)
                        break
                else:
                    print(2)
                    new = [{"typ": "default_roles", "roles": [{"name": role.name, "id": role.id}]}]
                    file.update(new)
            except Exception as a:
                print(a)
                file = [{"typ": "default_roles", "roles": [{"name": role.name, "id": role.id}]}]
                print(file)
            f.write(json.dumps(file))

    def rm_default_role(self, ctx: Context):
        pass


async def admin_setup(bot):
    """ Setup admin-commands """
    await bot.add_cog(Admin(bot))
    logging.getLogger("Basic_Logger").info(f"initialisation admin-commands finished")
