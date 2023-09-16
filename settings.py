import os

class StrategyParameters:
    def __init__(self, 
                 ema_period_4h_btc=50*4*60, 
                 ema_period_15m_btc=50*15, 
                 ema_period_4h_eth=50*4*60, 
                 ema_period_15m_eth=50*15, 
                 stop_loss_pct=1, 
                 take_profit_pct=3, 
                 rolling_window_size=31, 
                 top_coins_to_monitor=10, 
                 constant_monitoring_coins=5, 
                 periodic_monitoring_coins=5, 
                 backtest_start_date="YYYY-MM-DD", 
                 backtest_end_date="YYYY-MM-DD", 
                 leverage_level=1, 
                 auto_optimization=False, 
                 testnet=True):
        
        # Parametrii pentru BTC
        self.ema_period_4h_btc = ema_period_4h_btc
        self.ema_period_15m_btc = ema_period_15m_btc
        # Parametrii pentru ETH
        self.ema_period_4h_eth = ema_period_4h_eth
        self.ema_period_15m_eth = ema_period_15m_eth
        # Parametrii generali
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.rolling_window_size = rolling_window_size
        # Parametrii pentru API Binance
        self.api_key = os.environ.get("BINANCE_API_KEY")
        self.api_secret = os.environ.get("BINANCE_API_SECRET")
        # Parametrii pentru gestionarea monedelor
        self.top_coins_to_monitor = top_coins_to_monitor
        self.constant_monitoring_coins = constant_monitoring_coins
        self.periodic_monitoring_coins = periodic_monitoring_coins
        # Parametrii pentru optimizarea strategiei
        self.backtest_start_date = backtest_start_date
        self.backtest_end_date = backtest_end_date
        # Parametrii pentru tranzacționare cu levier
        self.leverage_level = leverage_level
        # Parametrii pentru optimizare automată (opțional)
        self.auto_optimization = auto_optimization
        # Parametrii pentru testare și implementare
        self.testnet = testnet
