"""Cryptor main script"""

import os
import requests
from dotenv import load_dotenv
from discord.ext import commands

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord")


class Cryptor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.binance = BinanceAPI()

    # Ping Binance servers to check connectivity
    @commands.command(help="Pings Binance server")
    async def pingcz(self, ctx):
        if self.binance.test_connectivity() != False:
            await ctx.send("funds are safu")

    # Get latest symbol price
    @commands.command(help="Displays the latest price of a symbol.")
    async def price(self, ctx, symbol):
        json_data = self.binance.get_price(symbol).json()
        if "code" in json_data:
            if json_data["code"] == -1100:
                await ctx.send("Invalid symbol. Format example: BTCUSDT")
            if json_data["code"] == -1121:
                await ctx.send("Pair does not exist.")
        elif "price" in json_data:
            await ctx.send(f"{symbol}: {float(json_data['price'])}")

    # Get the 24hr price change of a symbol
    @commands.command(
        help="Displays the 24hr. price change of a symbol.", aliases=["24change"]
    )
    async def change24(self, ctx, symbol):
        json_data = self.binance.get_24hrdata(symbol).json()
        if "code" in json_data:
            if json_data["code"] == -1100:
                await ctx.send("Invalid symbol. Format example: BTCUSDT")
            if json_data["code"] == -1121:
                await ctx.send("Pair does not exist.")
        else:
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


"""
# Command error handling
class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
"""


# Exception handling for HTTP GET requests
def exception_handler_get(func):
    def wrapper(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
            return False
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            return False
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            return False
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)
            return False
        else:
            return func(*args, **kwargs)

    return wrapper


class BinanceAPI:
    def __init__(self):
        self.BASE_URL = "https://api.binance.com/api2/"

    @exception_handler_get
    def test_connectivity(self):
        return requests.get(self.BASE_URL + "v3/ping", timeout=3)

    @exception_handler_get
    def get_price(self, symbol):
        payload = {"symbol": symbol}
        return requests.get(
            self.BASE_URL + "v3/ticker/price", params=payload, timeout=3
        )

    @exception_handler_get
    def get_24hrdata(self, symbol):
        payload = {"symbol": symbol}
        return requests.get(self.BASE_URL + "v3/ticker/24hr", params=payload, timeout=3)


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    bot.add_cog(Cryptor(bot))
    bot.run(TOKEN)