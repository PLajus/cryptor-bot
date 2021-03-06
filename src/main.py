""" Cryptor Bot set-up """

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands


activity = discord.Activity(type=discord.ActivityType.watching, name="charts | $help")
bot = commands.Bot(
    command_prefix="$",
    case_insensitive=True,
    activity=activity,
    status=discord.Status.online,
    help_command=None,
)

# Getting token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Loading cogs
if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(f"{dir_path}/cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    print(f"{bot.user.name} is online and ready.")


bot.run(TOKEN, bot=True, reconnect=True)