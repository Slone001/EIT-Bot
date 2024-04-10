import os
import time

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
    try:
        with open(f"{assets.files}{assets.cfg}") as file:
            Config = json.load(file)
    except json.decoder.JSONDecodeError as e:
        logger.critical(e)
        logger.critical(f"Config file is damaged, please delete the file or repair it")
        time.sleep(5)
        exit()
    bot_token = Config["Token"]
    if bot_token == "":
        logger.critical(f"no token is entered in config-file")
        time.sleep(5)
        exit()
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
    if not os.path.exists(assets.files):
        os.mkdir(assets.files)
    if not os.path.exists(assets.Logs):
        os.mkdir(assets.Logs)
    assets.logger_fun()
    logger = logging.getLogger("Basic_Logger")
    if not os.path.isfile(path=f"{assets.files}{assets.cfg}"):
        with open(f"{assets.files}{assets.cfg}", "w") as file:
            file.write(assets.config_blueprint())
        logger.critical(f"No token in {assets.files}{assets.cfg}.\nToken is required to start the bot")
        time.sleep(5)
        exit()
    if not os.path.isfile(path=f"{assets.files}{assets.data}"):
        with open(f"{assets.files}{assets.data}", "w") as file:
            file.write(assets.config_blueprint())
        logger.warning(f"No data file was found. New data-file will be created")
    main()

