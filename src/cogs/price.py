""" Price related commands cog """

from apis.binanceAPI import Binance
from discord.ext import commands


class Price(commands.Cog, name='Price Data'):
    def __init__(self, bot):
        self.bot = bot
        self.binance = Binance()

    # Get latest symbol price
    @commands.command(aliases=["p"], help="Displays the latest price of a symbol.")
    async def price(self, ctx, symbol):
        json_data = await self.binance.get_price(symbol)
        await ctx.send(f"{symbol}: {float(json_data['price'])}")

    # Get the 24hr price change of a symbol
    @commands.command(aliases=["24change", "c24"], help="Displays the 24hr. price change of a symbol.")
    async def change24(self, ctx, symbol):

        json_data = await self.binance.get_24hrdata(symbol)
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