from AlgorithmImports import *
from strategy import EnhancedStrategy, StrategyParameters
from config_loader import ConfigLoader
from leverage_manager import LeverageManager

config = ConfigLoader.load_config()
api_key = config["API_KEY"]
api_secret = config["API_SECRET"]




class MainAlgorithm(QCAlgorithm):

    def Initialize(self):
        # Setare date
        self.SetStartDate(2019, 1, 1)
        self.SetEndDate(2021, 2, 1)
        self.SetCash(10000)

        # Inițializare parametrii strategiei
        self.strategy_params = StrategyParameters()

        # Inițializare strategie
        self.strategy = EnhancedStrategy(self, self.strategy_params)
        # Inițializare LeverageManager cu levierul implicit (de exemplu, 1.0)
        self.leverage_manager = LeverageManager(self, default_leverage=1.0)

    def OnData(self, data):
        # Apelare funcție OnData din strategie
        self.strategy.OnFifteenMinuteData(data)
        self.strategy.OnFourHourData(data)
        # Setarea levierului pentru BTC la 2.0
        self.leverage_manager.set_leverage(self.btc, 2.0)

        # Obținerea levierului curent pentru BTC
        current_leverage = self.leverage_manager.get_leverage(self.btc)

        # Resetarea levierului pentru BTC la valoarea implicită
        self.leverage_manager.reset_leverage(self.btc)
