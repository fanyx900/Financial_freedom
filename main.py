from AlgorithmImports import *
from strategy import EnhancedStrategy, StrategyParameters
from config_loader import ConfigLoader

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

    def OnData(self, data):
        # Apelare funcție OnData din strategie
        self.strategy.OnFifteenMinuteData(data)
        self.strategy.OnFourHourData(data)
