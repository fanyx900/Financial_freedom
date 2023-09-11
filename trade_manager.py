import requests
from settings import StrategyParameters

class TradeManager:
    BASE_URL = "https://api.binance.com/api/v3"
    HEADERS = {
        "X-MBX-APIKEY": StrategyParameters().api_key
    }

    def __init__(self):
        self.settings = StrategyParameters()

    def _check_balance(self, symbol):
        endpoint = f"{self.BASE_URL}/account"
        response = requests.get(endpoint, headers=self.HEADERS)
        response.raise_for_status()
        balances = response.json()['balances']
        for balance in balances:
            if balance['asset'] == symbol:
                return float(balance['free'])
        return 0.0

    def place_buy_order(self, symbol, quantity):
        available_balance = self._check_balance(symbol)
        if available_balance < quantity:
            self.log(f"Insufficient balance. Available: {available_balance}, Required: {quantity}")
            return

        endpoint = f"{self.BASE_URL}/order"
        data = {
            "symbol": symbol,
            "side": "BUY",
            "type": "LIMIT",
            "quantity": quantity,
            # Add other required parameters like price, timestamp, etc.
        }
        response = requests.post(endpoint, headers=self.HEADERS, data=data)
        if response.status_code == 200:
            self.log(f"Buy order placed for {quantity} {symbol}")
        else:
            self.log(f"Error placing buy order for {symbol}: {response.text}")

    def place_sell_order(self, symbol):
        available_balance = self._check_balance(symbol)
        if available_balance <= 0:
            self.log(f"No {symbol} available to sell.")
            return

        endpoint = f"{self.BASE_URL}/order"
        data = {
            "symbol": symbol,
            "side": "SELL",
            "type": "LIMIT",
            "quantity": available_balance,
        }
        response = requests.post(endpoint, headers=self.HEADERS, data=data)
        if response.status_code == 200:
            self.log(f"Sell order placed for {available_balance} {symbol}")
        else:
            self.log(f"Error placing sell order for {symbol}: {response.text}")

    def place_short_order(self, symbol, quantity):
        available_balance = self._check_balance(symbol)
        if available_balance < quantity:
            self.log(f"Insufficient balance. Available: {available_balance}, Required: {quantity}")
            return

        # Logic for placing short order. This might require using Binance's futures API.

    def close_position(self, symbol):
        # Logic to close an open position for the given symbol.

    def set_leverage(self, symbol, leverage):
        # Logic to set leverage for the given symbol. This might require using Binance's futures API.

    def log(self, message):
        print(message)

    def notify(self, message):
        # Logic to send notifications, e.g., email or messages to a messaging app.
        pass
