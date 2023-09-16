from AlgorithmImports import *

# Indicatori pentru 4 ore
def ema50_4h_btc(algo, symbol):
    period = 50*4*60  # 50 bars of 4 hours in minutes
    return algo.EMA(symbol, period, Resolution.Minute)

def ema50_4h_eth(algo, symbol):
    period = 50*4*60  # 50 bars of 4 hours in minutes
    return algo.EMA(symbol, period, Resolution.Minute)

# Indicatori pentru 15 minute
def ema50_15m_btc(algo, symbol):
    period = 50*15  # 50 bars of 15 minutes
    return algo.EMA(symbol, period, Resolution.Minute)

def ema50_15m_eth(algo, symbol):
    period = 50*15  # 50 bars of 15 minutes
    return algo.EMA(symbol, period, Resolution.Minute)

# Calculul lumânărilor Heikin-Ashi
def heikin_ashi(algo, symbol, resolution=Resolution.Minute):
    history = algo.History(symbol, 2, resolution)
    if not history.empty:
        previous_bar = history.iloc[-2]
        current_bar = history.iloc[-1]
        
        ha_open = (previous_bar['open'] + previous_bar['close']) / 2
        ha_close = (current_bar['open'] + current_bar['close'] + current_bar['high'] + current_bar['low']) / 4
        ha_high = max(current_bar['high'], ha_open, ha_close)
        ha_low = min(current_bar['low'], ha_open, ha_close)
        
        return {'open': ha_open, 'close': ha_close, 'high': ha_high, 'low': ha_low}
    else:
        return None
