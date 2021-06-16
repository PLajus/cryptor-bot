# Cryptor main script

import os
import requests
from dotenv import load_dotenv
from discord.ext import commands


bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("{0.user} has connected to Discord".format(bot))


class Cryptor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.binance = BinanceAPI()

    # Ping Binance servers to check connectivity
    @commands.command(help="Pings Binance server")
    async def pingcz(self, ctx):
        if self.binance.test_connectivity() is not None:
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
                    f"{symbol} price pumped by: {price_change} and {json_data['priceChangePercent']}%"
                )
            elif price_change < 0:
                await ctx.send(
                    f"{symbol} price dumped by: {price_change} and {json_data['priceChangePercent']}%"
                )
            else:
                await ctx.send(
                    f"{symbol} price did not change in 24hrs. Use !price to find out current price."
                )


class BinanceAPI:
    def __init__(self):
        self.BASE_URL = "https://api.binance.com/api/"

    def test_connectivity(self):
        return requests.get(self.BASE_URL + "v3/ping")

    def get_price(self, symbol):
        payload = {"symbol": symbol}
        return requests.get(self.BASE_URL + "v3/ticker/price", params=payload)

    def get_24hrdata(self, symbol):
        payload = {"symbol": symbol}
        return requests.get(self.BASE_URL + "v3/ticker/24hr", params=payload)


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    bot.add_cog(Cryptor(bot))
    bot.run(TOKEN)