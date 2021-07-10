"""Miscellaneous commands cog"""

from discord.ext import commands
from apis.binanceAPI import Binance


class Misc(commands.Cog, name="Misc"):
    def __init__(self, bot):
        self.bot = bot
        self.binance = Binance()

    # Ping Binance servers to check connectivity
    @commands.command(help="Pings Binance server.")
    async def pingcz(self, ctx):
        if await self.binance.ping_binance() == 200:
            await ctx.send("funds are safu")


def setup(bot):
    bot.add_cog(Misc(bot))
