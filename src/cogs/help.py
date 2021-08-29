"""Custom Help command cog"""

from inspect import signature
from discord.ext import commands
import discord
from discord.errors import Forbidden


async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("I can't send embeds. Please check my permissions.")
        except Forbidden:
            await ctx.author.send(
                f"I can't send messages in **# {ctx.channel.name}** on {ctx.guild.name}.\n",
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

    # General help
    @commands.command()
    async def help(self, ctx, *input):
        if not input:
            embed = discord.Embed(
                title="Cryptor Commands",
                description="Command prefix is `$`",
                colour=discord.Colour.dark_green(),
            )
            embed.set_footer(
                text="\u200b\nFor more information use $help <command>",
            )
            embed.set_author(
                name="Author",
                url="https://github.com/PLajus",
                icon_url="https://avatars.githubusercontent.com/u/77925599?s=400&v=4",
            )
            hidden_cogs = ["Help", "ErrorHandler"]

            # Goes through all non hidden cogs and lists their commands.
            for cog in self.bot.cogs:
                if cog not in hidden_cogs:
                    commands = ""
                    for command in self.bot.get_cog(cog).get_commands():
                        commands += f"`{command.name}`, "
                    embed.add_field(name=cog, value=commands[0:-2], inline=False)

        else:
            if len(input) == 1:
                command = self.bot.get_command(input[0].lower())
                if command is not None:
                    embed = discord.Embed(
                        title=f"Help | {command.name}",
                        description=command.help,
                        colour=discord.Colour.dark_green(),
                    )
                    cmd_aliases = ""
                    for alias in command.aliases:
                        cmd_aliases += f", `{alias}`"

                    embed.add_field(
                        name="\u200b\nTriggers:",
                        value=f"`{command.qualified_name}`{cmd_aliases}",
                        inline=False,
                    )

                    embed.add_field(
                        name="Usage:",
                        value=f"`${command.qualified_name} {command.signature}`",
                        inline=False,
                    )

                    if command.name == "pingcz":
                        embed.add_field(
                            name="Use Example:",
                            value=f"`${command.qualified_name}`",
                            inline=False,
                        )

                    elif command.name == "orders":
                        embed.add_field(
                            name="Use Example:",
                            value=f"`${command.qualified_name} BTCUSDT`\n`${command.qualified_name} BTCUSDT 5 asks`\n`${command.qualified_name} ETHUSDT 10 bids`",
                            inline=False,
                        )

                    elif command.name == "history":
                        embed.add_field(
                            name="Use Example:",
                            value=f"`${command.qualified_name} BTCUSDT yyyy-mm-dd`\n`${command.qualified_name} BTCUSDT 2021-08-15`",
                            inline=False,
                        )

                    else:
                        embed.add_field(
                            name="Use Example:",
                            value=f"`${command.qualified_name} BTCUSDT`",
                            inline=False,
                        )

                else:
                    embed = discord.Embed(
                        title="Huh whuh?",
                        description=f"Command or category `{input[0]}` does not exist.",
                        colour=discord.Colour.red(),
                    )

            else:
                embed = discord.Embed(
                    title="Too many requests.",
                    description="Please request one command at a time.",
                    color=discord.Color.orange(),
                )
        await send_embed(ctx, embed)


def setup(bot):
    bot.add_cog(Help(bot))