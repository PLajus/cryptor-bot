"""Cryptor main script"""

import os
import binanceAPI
from dotenv import load_dotenv
from discord.ext import commands

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord")


class Cryptor(commands.Cog):
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

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    dir_path = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(f"{dir_path}/cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    bot.add_cog(Cryptor(bot))
    bot.run(TOKEN)