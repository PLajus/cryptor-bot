""" Price related commands cog """

from apis.binanceAPI import Binance
from discord.ext import commands
import calendar
import datetime


async def get_unix_ms_from_date(date):
    return int(calendar.timegm(date.timetuple()) * 1000 + date.microsecond / 1000)


class Price(commands.Cog, name="Price Data"):
    def __init__(self, bot):
        self.bot = bot
        self.binance = Binance()

    # Get latest symbol price
    @commands.command(aliases=["p"], help="Displays the latest price of a symbol.")
    async def price(self, ctx, symbol):
        symbol = symbol.upper()
        json_data = await self.binance.get_price(symbol)
        await ctx.send(f"{symbol}: {float(json_data['price'])}")

    # Get the 24hr price change of a symbol
    @commands.command(
        aliases=["24change", "c24"], help="Displays the 24hr. price change of a symbol."
    )
    async def change24(self, ctx, symbol):
        symbol = symbol.upper()
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

    # Get the price of a symbol at a past date
    @commands.command(
        aliases=["h"],
        help="Displays the price of a Symbol at a past date. Price is shown at 12:00:00 AM GMT of specified date.",
    )
    async def history(self, ctx, symbol, date):
        symbol = symbol.upper()
        format = "%Y-%m-%d"

        try:
            datime_date = datetime.datetime.strptime(date, format)
        except ValueError:
            await ctx.send("Incorrect date format. It should be `yyyy-mm-dd`.")
            return

        today = datetime.date.today()
        if datime_date > datetime.datetime(
            year=today.year, month=today.month, day=today.day
        ):
            await ctx.send("I'm afraid that I cannot predict the future... yet.")
            return

        if datime_date < datetime.datetime(year=2017, month=9, day=3):
            await ctx.send("Oldest date I can go back to is **2017-09-03**.")
            return

        str_date = datime_date.strftime("%m/%d/%Y")
        start_date = await get_unix_ms_from_date(
            datetime.datetime.strptime(str_date, "%m/%d/%Y")
        )

        end_date = await get_unix_ms_from_date(
            datetime.datetime.strptime(str_date, "%m/%d/%Y")
            + datetime.timedelta(minutes=1)
        )
        json_data = await self.binance.get_history(symbol, start_date, end_date)
        await ctx.send(
            f"Price of **{symbol}** at *{date}*: `{float(json_data[0]['p'])}`"
        )


def setup(bot):
    bot.add_cog(Price(bot))