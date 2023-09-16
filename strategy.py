from AlgorithmImports import *
from QuantConnect.Data.Market import TradeBar
from QuantConnect.Indicators import *
from QuantConnect import Resolution
from datetime import datetime, time
from settings import StrategyParameters
from indicators import ema50_4h_btc, ema50_4h_eth, ema50_15m_btc, ema50_15m_eth
from trade_manager import TradeManager

class EnhancedStrategy:
    def __init__(self, algo, params):
        self.algo = algo
        self.params = params
        self.trade_manager = TradeManager(self.algo, self.params)

        # Simboluri
        self.btc = self.algo.AddCrypto("BTCUSD", Resolution.Minute).Symbol
        self.eth = self.algo.AddCrypto("ETHUSD", Resolution.Minute).Symbol

        # Indicatori pentru BTC și ETH
        self.ema50_4h_btc = self.algo.EMA(self.btc, self.params.ema_period_4h_btc, Resolution.Minute)
        self.ema50_4h_eth = self.algo.EMA(self.eth, self.params.ema_period_4h_eth, Resolution.Minute)
        self.ema50_15m_btc = self.algo.EMA(self.btc, self.params.ema_period_15m_btc, Resolution.Minute)
        self.ema50_15m_eth = self.algo.EMA(self.eth, self.params.ema_period_15m_eth, Resolution.Minute)

        # Adăugăm indicatorul RSI pentru BTC și ETH
        self.rsi_btc = self.algo.RSI(self.btc, 14, MovingAverageType.Wilders, Resolution.Minute, Field.Close)
        self.rsi_eth = self.algo.RSI(self.eth, 14, MovingAverageType.Wilders, Resolution.Minute, Field.Close)

        # Adăugăm Average True Range pentru calculul stop loss și take profit
        self.atr_btc = self.algo.ATR(self.btc, 14, MovingAverageType.Wilders, Resolution.Minute)
        self.atr_eth = self.algo.ATR(self.eth, 14, MovingAverageType.Wilders, Resolution.Minute)

        # Inițializare a nivelurilor de suport și rezistență
        self.support_levels_btc = 0
        self.resistance_levels_btc = 0
        self.support_levels_eth = 0
        self.resistance_levels_eth = 0

        # Lumânări anterioare pentru BTC și ETH
        self.previous_btc = None
        self.previous_eth = None

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

        # Verificăm dacă RSI este într-o zonă de supra-cumpărat sau supra-vândut
        rsi_overbought_btc = self.rsi_btc.Current.Value > 70
        rsi_oversold_btc = self.rsi_btc.Current.Value < 30
        rsi_overbought_eth = self.rsi_eth.Current.Value > 70
        rsi_oversold_eth = self.rsi_eth.Current.Value < 30

        # Apelare funcție de tranzacționare
        self.trade_manager.ExecuteTrades(data, self.btc, self.ema50_4h_btc, self.ema50_15m_btc, double_top_btc, double_bottom_btc, bullish_engulfing_btc, bearish_engulfing_btc, near_support_btc, near_resistance_btc, rsi_overbought_btc, rsi_oversold_btc)
        self.trade_manager.ExecuteTrades(data, self.eth, self.ema50_4h_eth, self.ema50_15m_eth, double_top_eth, double_bottom_eth, bullish_engulfing_eth, bearish_engulfing_eth, near_support_eth, near_resistance_eth, rsi_overbought_eth, rsi_oversold_eth)

        # Actualizare lumânări anterioare pentru BTC și ETH
        self.previous_btc = data[self.btc]
        self.previous_eth = data[self.eth]
