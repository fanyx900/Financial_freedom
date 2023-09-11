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

    def place_buy_order(self, symbol, quantity, stop_loss_pct=None, take_profit_pct=None):
        available_balance = self._check_balance(symbol)
        if available_balance < quantity:
            self.log(f"Insufficient balance. Available: {available_balance}, Required: {quantity}")
            return

        # Logic to place buy order on Binance
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

        # Logic to place sell order on Binance
        endpoint = f"{self.BASE_URL}/order"
        data = {
            "symbol": symbol,
            "side": "SELL",
            "type": "LIMIT",
            "quantity": available_balance,
            # Add other required parameters like price, timestamp, etc.
        }
        response = requests.post(endpoint, headers=self.HEADERS, data=data)
        if response.status_code == 200:
            self.log(f"Sell order placed for {available_balance} {symbol}")
        else:
            self.log(f"Error placing sell order for {symbol}: {response.text}")

    # Implement similar logic for place_short_order and close_position

    def set_leverage(self, symbol, leverage):
        # Logic to set leverage on Binance
        # Note: This might require using Binance's futures API
        pass

    def log(self, message):
        # Simple logging to console for now
        print(message)

    def notify(self, message):
        # Implement notification logic here (e.g. send an email or a message to a messaging app)
        pass
