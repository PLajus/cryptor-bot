"""Miscellaneous commands cog"""

from discord.ext import commands
import discord
from apis.binanceAPI import Binance

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.binance = Binance()

    @commands.Cog.listener()   
    async def on_message(self, ctx):
        if self.bot.user.mentioned_in(ctx) and not ctx.mention_everyone:
            await ctx.channel.send("Please use $help to view my commands.")

    # Ping Binance servers to check connectivity
    @commands.command(help="Pings Binance server", aliases=["pingCZ"])
    async def pingcz(self, ctx):
        if self.binance.test_connectivity().status_code == 200:
            await ctx.send("funds are safu")


def setup(bot):
    bot.add_cog(Misc(bot))
