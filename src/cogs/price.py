""" Price related commands cog """

import binanceAPI
from discord.ext import commands


class Price(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.binance = binanceAPI.Binance()

    # Ping Binance servers to check connectivity
    @commands.command(help="Pings Binance server", aliases=["pingCZ"])
    async def pingcz(self, ctx):
        if self.binance.test_connectivity().status_code == 200:
            await ctx.send("funds are safu")

    # Get latest symbol price
    @commands.command(help="Displays the latest price of a symbol.")
    async def price(self, ctx, symbol):
        json_data = self.binance.get_price(symbol).json()
        await ctx.send(f"{symbol}: {float(json_data['price'])}")

    # Get the 24hr price change of a symbol
    @commands.command(
        help="Displays the 24hr. price change of a symbol.", aliases=["24change"]
    )
    async def change24(self, ctx, symbol):

        json_data = self.binance.get_24hrdata(symbol).json()
        price_change = float(json_data["priceChange"])

        if price_change > 0:
            await ctx.send(
                f"{symbol} price pumped by: {price_change} ({json_data['priceChangePercent']}%)"
            )
        elif price_change < 0:
            await ctx.send(
                f"{symbol} price dumped by: {price_change} ({json_data['priceChangePercent']}%)"
            )
        else:
            await ctx.send(
                f"{symbol} price did not change in 24hrs. Use !price to find out the current price."
            )


def setup(bot):
    bot.add_cog(Price(bot))