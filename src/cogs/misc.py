"""Miscellaneous commands cog"""

from apis.binanceAPI import Binance
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.binance = Binance()

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message):
            await message.channel.send("Please use $help to view my commands.")

    # Ping Binance servers to check connectivity
    @commands.command(help="Pings Binance server", aliases=["pingCZ"])
    async def pingcz(self, ctx):
        if self.binance.test_connectivity().status_code == 200:
            await ctx.send("funds are safu")


def setup(bot):
    bot.add_cog(Misc(bot))
