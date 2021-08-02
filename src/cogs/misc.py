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

    @commands.command(aliases=["o"], help="Displays current bids and asks.")
    async def orders(self, ctx, symbol, amount=1, order_type=None):

        if order_type is not None and order_type.lower() not in ["bids", "asks"]:
            await ctx.send(
                f"Order type `{order_type}` does not exist. Please use asks/bids."
            )
            return

        if amount < 0 or amount > 5:
            await ctx.send("Invalid order amount. Please choose from 1 to 5.")
            return

        symbol = symbol.upper()
        json_data = await self.binance.get_orders(symbol)

        if order_type is not None:
            order_type = order_type.lower()
            await ctx.send(f"**{order_type.capitalize()}:**")
            for item in json_data[order_type][:amount]:
                price, qty = item
                await ctx.send(f"Price: `{price}`\nAmount: `{qty}`")

        else:
            await ctx.send("**Bids:**\n")
            for item in json_data["bids"][:amount]:
                b_price, b_qty = item
                await ctx.send(f"Price: `{b_price}`\nAmount: `{b_qty}`")
            await ctx.send("**Asks:**\n")
            for item in json_data["asks"][:amount]:
                a_price, a_qty = item
                await ctx.send(f"Price: `{a_price}`\nAmount: `{a_qty}`")


def setup(bot):
    bot.add_cog(Misc(bot))
