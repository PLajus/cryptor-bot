"""Binance API requests module"""

import requests

# Exception handling for HTTP GET requests
def exception_handler_get(func):
    def wrapper(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
            r.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP Error: {http_err}")
            raise http_err
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
            raise errc
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
            raise errt
        except Exception as err:
            print(f"Something went wrong: {err}")
            raise err
        else:
            return func(*args, **kwargs)

    return wrapper


class Binance:
    def __init__(self):
        self.BASE_URL = "https://api.binance.com/api/"

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