import requests
import logging
from settings import StrategyParameters

class TradeManager:
    BASE_URL = "https://api.binance.com/api/v3"
    FUTURES_URL = "https://fapi.binance.com/fapi/v1"  # Binance Futures API endpoint
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
        # For short orders, we'll use Binance's Futures API
        endpoint = f"{self.FUTURES_URL}/order"
        data = {
            "symbol": symbol,
            "side": "SELL",
            "type": "LIMIT",
            "quantity": quantity,
            # Add other required parameters like price, timestamp, etc.
        }
        response = requests.post(endpoint, headers=self.HEADERS, data=data)
        if response.status_code == 200:
            self.log(f"Short order placed for {quantity} {symbol}")
        else:
            self.log(f"Error placing short order for {symbol}: {response.text}")

    def close_position(self, symbol):
        # To close a position, we'll sell the entire quantity of the asset
        available_balance = self._check_balance(symbol)
        if available_balance <= 0:
            self.log(f"No {symbol} position to close.")
            return

        self.place_sell_order(symbol)

    def set_leverage(self, symbol, leverage):
        # Setting leverage using Binance's Futures API
        endpoint = f"{self.FUTURES_URL}/leverage"
        data = {
            "symbol": symbol,
            "leverage": leverage
        }
        response = requests.post(endpoint, headers=self.HEADERS, data=data)
        if response.status_code == 200:
            self.log(f"Leverage set to {leverage} for {symbol}")
        else:
            self.log(f"Error setting leverage for {symbol}: {response.text}")

    def log(message, level="info"):
        # Configurarea logger-ului
        logging.basicConfig(filename='trade_manager.log', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Înregistrarea mesajului în funcție de nivelul de severitate
        if level == "debug":
            logging.debug(message)
        elif level == "info":
            logging.info(message)
        elif level == "warning":
            logging.warning(message)
        elif level == "error":
            logging.error(message)
        elif level == "critical":
            logging.critical(message)