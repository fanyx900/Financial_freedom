from AlgorithmImports import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import *
from QuantConnect import Resolution
from datetime import datetime, time
from settings import StrategyParameters
from indicators import ema50_4h_btc, ema50_4h_eth, ema50_15m_btc, ema50_15m_eth
from trade_manager import TradeManager

class BinanceFeeModel(FeeModel):
    def GetOrderFee(self, parameters):
        fee = parameters.Order.AbsoluteQuantity * 0.0001  # 0.01% fee
        return OrderFee(CashAmount(fee, parameters.Security.Price.Currency))

class EnhancedStrategy:
    def __init__(self, algo, params: StrategyParameters):
        self.algo = algo
        self.params = params
        self.trade_manager = TradeManager(self.algo, self.params)

        # Simboluri
        self.btc = self.algo.AddCrypto("BTCUSD", Resolution.Minute).Symbol
        self.eth = self.algo.AddCrypto("ETHUSD", Resolution.Minute).Symbol
       
        # Setare model de comision personalizat
        self.algo.Securities[self.btc].FeeModel = BinanceFeeModel()
        self.algo.Securities[self.eth].FeeModel = BinanceFeeModel()

        # Inițializare a nivelurilor de suport și rezistență
        self.support_levels_btc = 0
        self.resistance_levels_btc = 0
        self.support_levels_eth = 0
        self.resistance_levels_eth = 0

        # Lumânări anterioare pentru BTC și ETH
        self.previous_btc = None
        self.previous_eth = None

        # Indicatori pentru 4 ore
        self.ema50_4h_btc = self.algo.EMA(self.btc, self.params.ema_period_4h_btc, Resolution.Minute)
        self.ema50_4h_eth = self.algo.EMA(self.eth, self.params.ema_period_4h_eth, Resolution.Minute)

        # Indicatori pentru 15 minute
        self.ema50_15m_btc = self.algo.EMA(self.btc, self.params.ema_period_15m_btc, Resolution.Minute)
        self.ema50_15m_eth = self.algo.EMA(self.eth, self.params.ema_period_15m_eth, Resolution.Minute)

        # Rolling windows pentru detectarea dublu top/bottom și pentru suport/rezistență
        self.highs_btc = RollingWindow[float](self.params.rolling_window_size)
        self.lows_btc = RollingWindow[float](self.params.rolling_window_size)
        self.highs_eth = RollingWindow[float](self.params.rolling_window_size)
        self.lows_eth = RollingWindow[float](self.params.rolling_window_size)

    def OnFourHourData(self, data):
        # Actualizare Rolling Windows pentru suport/rezistență
        self.highs_btc.Add(data[self.btc].High)
        self.lows_btc.Add(data[self.btc].Low)
        self.highs_eth.Add(data[self.eth].High)
        self.lows_eth.Add(data[self.eth].Low)

        # Calculare zone de suport și rezistență
        self.support_levels_btc = min(self.lows_btc)
        self.resistance_levels_btc = max(self.highs_btc)
        self.support_levels_eth = min(self.lows_eth)
        self.resistance_levels_eth = max(self.highs_eth)

    def OnFifteenMinuteData(self, data):
        # Detectare dublu top/bottom pentru BTC și ETH
        double_top_btc = self.highs_btc[0] > self.highs_btc[1] and self.highs_btc[0] > self.highs_btc[2]
        double_bottom_btc = self.lows_btc[0] < self.lows_btc[1] and self.lows_btc[0] < self.lows_btc[2]
        double_top_eth = self.highs_eth[0] > self.highs_eth[1] and self.highs_eth[0] > self.highs_eth[2]
        double_bottom_eth = self.lows_eth[0] < self.lows_eth[1] and self.lows_eth[0] < self.lows_eth[2]

        # Detectare bullish engulfing pentru BTC și ETH
        bullish_engulfing_btc = self.previous_btc and data[self.btc].Close > self.previous_btc.Close and data[self.btc].Open < self.previous_btc.Open
        bullish_engulfing_eth = self.previous_eth and data[self.eth].Close > self.previous_eth.Close and data[self.eth].Open < self.previous_eth.Open

        # Detectare bearish engulfing pentru BTC și ETH
        bearish_engulfing_btc = self.previous_btc and data[self.btc].Close < self.previous_btc.Close and data[self.btc].Open > self.previous_btc.Open
        bearish_engulfing_eth = self.previous_eth and data[self.eth].Close < self.previous_eth.Close and data[self.eth].Open > self.previous_eth.Open

        # Verificăm dacă dublu top/bottom se află în apropierea zonelor de suport/rezistență
        near_support_btc = data[self.btc].Close <= self.support_levels_btc * 1.02
        near_resistance_btc = data[self.btc].Close >= self.resistance_levels_btc * 0.98
        near_support_eth = data[self.eth].Close <= self.support_levels_eth * 1.02
        near_resistance_eth = data[self.eth].Close >= self.resistance_levels_eth * 0.98

        # Apelare funcție de tranzacționare
        self.trade_manager.ExecuteTrades(data, self.btc, self.ema50_4h_btc, self.ema50_15m_btc, double_top_btc, double_bottom_btc, bullish_engulfing_btc, bearish_engulfing_btc, near_support_btc, near_resistance_btc)
        self.trade_manager.ExecuteTrades(data, self.eth, self.ema50_4h_eth, self.ema50_15m_eth, double_top_eth, double_bottom_eth, bullish_engulfing_eth, bearish_engulfing_eth, near_support_eth, near_resistance_eth)

        # Actualizare lumânări anterioare pentru BTC și ETH
        self.previous_btc = data[self.btc]
        self.previous_eth = data[self.eth]
