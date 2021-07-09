""" Binance API requests """

import aiohttp


class Binance:
    def __init__(self):
        self.BASE_URL = "https://api.binance.com/api/"

    async def ping_binance(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.BASE_URL + "v3/ping", raise_for_status=True
            ) as response:
                return await response.status

    async def get_price(self, symbol):
        params = {"symbol": symbol}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.BASE_URL + "v3/ticker/price", params=params, raise_for_status=True
            ) as response:
                return await response.json()

    async def get_24hrdata(self, symbol):
        params = {"symbol": symbol}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.BASE_URL + "v3/ticker/24hr", params=params, raise_for_status=True
            ) as response:
                return await response.json()