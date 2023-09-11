import requests

class DataManager:
    BASE_URL = "https://api.binance.com/api/v3"

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def fetch_data(self, symbol, interval, limit=100):
        endpoint = f"{self.BASE_URL}/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_top_coins_by_volume(self, limit=10):
        endpoint = f"{self.BASE_URL}/ticker/24hr"
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            coins = response.json()
            sorted_coins = sorted(coins, key=lambda x: float(x['quoteVolume']), reverse=True)
            return [coin['symbol'] for coin in sorted_coins[:limit]]
        else:
            response.raise_for_status()
