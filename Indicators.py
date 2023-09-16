from AlgorithmImports import *

def calculate_ema(algo, symbol, period_multiplier, base_period=50, resolution=Resolution.Minute):
    """
    Calculează EMA pentru un simbol dat și o perioadă specificată.
    
    Args:
    - algo: Instanța algoritmului QCAlgorithm.
    - symbol: Simbolul pentru care se calculează EMA.
    - period_multiplier: Multiplier pentru perioada de bază.
    - base_period: Perioada de bază pentru EMA (implicit 50).
    - resolution: Rezoluția datelor (implicit Minute).
    
    Returns:
    - EMA pentru simbolul și perioada specificată.
    """
    period = base_period * period_multiplier
    return algo.EMA(symbol, period, resolution)

def heikin_ashi(algo, symbol, resolution=Resolution.Minute):
    """
    Calculează lumânările Heikin-Ashi pentru un simbol dat.
    
    Args:
    - algo: Instanța algoritmului QCAlgorithm.
    - symbol: Simbolul pentru care se calculează lumânările Heikin-Ashi.
    - resolution: Rezoluția datelor (implicit Minute).
    
    Returns:
    - Lumânările Heikin-Ashi sau None dacă nu există date istorice.
    """
    try:
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
    except Exception as e:
        algo.Debug(f"Error calculating Heikin-Ashi for {symbol}: {e}")
        return None
