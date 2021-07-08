"""Miscellaneous commands cog"""

from discord.ext import commands
from apis.binanceAPI import Binance


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.binance = Binance()

    # Ping Binance servers to check connectivity
    @commands.command(help="Pings Binance server")
    async def pingcz(self, ctx):
        if self.binance.test_connectivity().status_code == 200:
            await ctx.send("funds are safu")


def setup(bot):
    bot.add_cog(Misc(bot))
