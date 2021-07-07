from discord.ext import commands
import discord
from discord.errors import Forbidden


async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("I'm unable to send embeds. Please check my permissions.")
        except Forbidden:
            await ctx.author.send(
                f"I am unable to send messages in {ctx.channel.name} on {ctx.guild.name}\n",
                embed=embed,
            )


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot responds when mentioned
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if self.bot.user.mentioned_in(ctx) and not ctx.mention_everyone:
            await ctx.channel.send("Please use $help to view my commands.")

    @commands.command(help="Shows this message")
    async def help(self, ctx, message=None):
        embed = discord.Embed(colour=discord.Colour.dark_green())

        # General help
        if message is None:
            embed.title = "Cryptor Commands"
            embed.description = "Command prefix is `$`"
            embed.set_footer(
                text="\u200b\nFor more information use $help <command> or $help <category>"
            )

            embed.set_author(
                name="Author",
                url="https://github.com/PLajus",
                icon_url="https://avatars.githubusercontent.com/u/77925599?s=400&v=4",
            )
            embed.add_field(
                name=":bar_chart: Price Data", value="`$help pricedata`", inline=False
            )
            embed.add_field(name=":toolbox: Misc", value="`$help misc`")

        # Price data category help
        elif message == "pricedata":
            embed.title = "Price Data Commands :bar_chart:"
            embed.description = "\u200b\n**`price`**, **`change24`**"
            embed.set_footer(text="\u200b\nFor more information use $help <command>")

        # Price command help
        elif message == "price" or message == "p":
            embed.title = "price"
            embed.description = "Displays the latest price of a symbol."

            embed.add_field(name="Triggers", value="`price, p`", inline=False)

            embed.add_field(name="Usage", value="`$price <SYMBOL>`", inline=False)

            embed.add_field(
                name="Use Examples",
                value="`$price BTCUSDT\n$p ADAETH`",
                inline=False,
            )

        # Change24 command help
        elif message == "change24" or message == "c24":
            embed.title = "change24"
            embed.description = "Displays the 24hr. price change of a symbol."

            embed.add_field(name="Triggers", value="`change24, c24`", inline=False)

            embed.add_field(name="Usage", value="`$change24 <SYMBOL>`", inline=False)

            embed.add_field(
                name="Use Examples",
                value="`$change24 BTCUSDT\n$c24 ADAETH`",
                inline=False,
            )

        # Mics category help
        elif message == "misc":
            embed.title = "Mics Commands :toolbox:"
            embed.description = "\u200b\n**`pingcz`**"
            embed.set_footer(text="\u200b\nFor more information use $help <command>")

        # Pingcz command help
        elif message.lower() == "pingcz":
            embed.title = "pingcz"
            embed.description = "Pings Binance server to test connectivity."

            embed.add_field(name="Triggers", value="`pingcz, pingCZ`", inline=False)

            embed.add_field(name="Usage", value="`$pingcz`", inline=False)

            embed.add_field(
                name="Use Examples",
                value="`$pingcz`",
                inline=False,
            )

        else:
            embed.colour = discord.Colour.red()
            embed.title = f"Huh whuh?"
            embed.description = f"Command or category `{message}` does not exist."

        await send_embed(ctx, embed)


def setup(bot):
    bot.add_cog(Help(bot))