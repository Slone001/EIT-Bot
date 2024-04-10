import os
import discord
from discord.ext import commands
import asyncio
import sys
import logging
import assets
import json

"""" Version 1.0.0 ; Date: 10.04.2024 """

""" Global Var """

bot_prefix = None
if sys.platform == "win32":
    bot_prefix = "§test "
elif sys.platform == "linux":
    bot_prefix = "!test "
else:
    bot_prefix = "test "
    print(f"Loaded prefix for {sys.platform}. Prefix is {bot_prefix}")


""" Bot Starting """

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.presences = True
intents.reactions = True
bot = commands.Bot(
    command_prefix=bot_prefix,
    case_insensitive=False,
    help_command=None,
    intents=intents)


def main():
    global logger
    Config = json.load()
    bot_token = Config["Token"]
    logger.info(f"Bot is starting")
    logger.info(f"Bot prefix is {bot_prefix}")
    asyncio.run(bot_start(bot_token))


async def bot_start(bot_token):
    await bot.start(bot_token)


@bot.event
async def on_ready():
    logger.info(f"Loading Cogs")
    await cogs_loader()
    await slash_cogs()
    logger.info(f"Start sync")
    synced = await bot.tree.sync()
    for x in synced:
        logger.info(f"Loaded command: {x}")
    logger.info(f"All cogs loaded")


async def cogs_loader():
    pass

async def slash_cogs():
    pass


if __name__ == '__main__':
    global logger
    assets.logger_fun()
    logger = logging.getLogger("Basic_Logger")
    if not os.path.exists(assets.files):
        os.mkdir(assets.files)
    if not os.path.exists(assets.Logs):
        os.mkdir(assets.Logs)
    if not os.path.isfile(path=f"{assets.files}{assets.cfg}"):
        with open(f"{assets.files}{assets.cfg}", "w") as file:
            file.write(assets.config_blueprint())
        logger.critical(f"No token in {assets.files}{assets.cfg}.\nToken is required to start the bot")
        exit()
    main()

