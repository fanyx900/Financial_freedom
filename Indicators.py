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
