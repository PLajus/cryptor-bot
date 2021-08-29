""" Error handling cog """

import discord
from discord.ext import commands
import aiohttp
import asyncio


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if ctx.command.has_error_handler() or ctx.cog.has_error_handler():
            return

        ignored_errs = commands.CommandNotFound

        # Check for original exceptions raised and sent to CommandInvokeError
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

        elif isinstance(error, aiohttp.ClientResponseError):
            if error.code == 400:
                await ctx.send("Symbol could not be found.")
            else:
                print(f"There was en error: {error.code} {error.message}")
                await ctx.send(
                    f"There was an Error: {error.code} {error.message}. Please try again later."
                )

        elif isinstance(error, aiohttp.ClientConnectionError):
            print(f"There was en error: {error.code} {error.message}")
            await ctx.send("There was a Connection Error. Please try again later.")

        elif isinstance(
            error,
            aiohttp.ClientPayloadError,
        ):
            print(f"There was en error: {error.code} {error.message}")
            await ctx.send("There was an Error. Please try again later.")

        elif isinstance(error, asyncio.TimeoutError):
            await ctx.send("There was a Timeout Error. Please try again later.")

        else:
            print(f"There was en error: {error}")
            await ctx.send("Something went wrong.")


def setup(bot):
    bot.add_cog(ErrorHandler(bot))