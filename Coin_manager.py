from AlgorithmImports import *
import requests

class CoinManager:
    def __init__(self, algo):
        self.algo = algo
        self.top_coins = []
        self.active_coins = []
        self.backup_coins = []

    def update_top_coins(self):
        # Aici vom interoga API-ul Binance pentru a obține top 10 monede după volum
        # De exemplu, folosind un endpoint precum 'https://api.binance.com/api/v3/ticker/24hr'
        # și sortând rezultatele după volumul de tranzacționare.

        # NOTĂ: Acesta este doar un pseudocod și ar trebui adaptat în funcție de structura datelor returnate de API.
        response = requests.get('https://api.binance.com/api/v3/ticker/24hr')
        coins = response.json()
        sorted_coins = sorted(coins, key=lambda x: x['quoteVolume'], reverse=True)
        self.top_coins = [coin['symbol'] for coin in sorted_coins[:10]]

    def set_active_coins(self):
        # Aici vom seta monedele active pe care le vom monitoriza activ
        self.active_coins = self.top_coins[:5]

    def set_backup_coins(self):
        # Aici vom seta monedele de rezervă pe care le vom verifica la începutul fiecărei zile
        self.backup_coins = self.top_coins[5:]

    def get_active_coins(self):
        return self.active_coins

    def get_backup_coins(self):
        return self.backup_coins
