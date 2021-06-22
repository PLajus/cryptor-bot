""" Error handling"""

import discord
import traceback
import sys
from discord.ext import commands


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"):
            return

        await ctx.send(f"There was an error: {error}")

        
def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))