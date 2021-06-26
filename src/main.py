""" Cryptor Bot set-up """

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

# Loading cogs
if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(f"{dir_path}/cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

# Getting token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print(f"{bot.user.name} is online and ready.")


bot.run(TOKEN, bot=True, reconnect=True)