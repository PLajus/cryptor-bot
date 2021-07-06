""" Error handling cog """

import discord
from discord.ext import commands
from requests.exceptions import Timeout
from requests.models import HTTPError


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if ctx.command.has_error_handler() or ctx.cog.has_error_handler():
            return

        ignored_errs = commands.CommandNotFound

        # Allows to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found, keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        # Igored errors are silenced
        if isinstance(error, ignored_errs):
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(
                    f"{ctx.command} can not be used in Private Messages."
                )
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Required argument is missing.")

        elif isinstance(error, HTTPError):
            try:
                if error.response.json()["code"] == -1100:
                    await ctx.send("Symbol has invalid characters or needs to be in upper case.")
                else:
                    await ctx.send(error.response.json()["msg"])
            except ValueError:
                await ctx.send(f"There was an HTTP error: {error.response.status_code}")

        elif isinstance(error, ConnectionError):
            await ctx.send("There was a Connection Error. Please try again later.")

        elif isinstance(error, Timeout):
            await ctx.send("There was a Timeout Error. Please try again later.")

        # All other errors
        else:
            print(f"There was en error: {error}")
            await ctx.send("Something went wrong.")


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))