class StrategyParameters:
    def __init__(self):
        # Parametrii pentru BTC
        self.ema_period_4h_btc = 50*4*60
        self.ema_period_15m_btc = 50*15
        # Parametrii pentru ETH
        self.ema_period_4h_eth = 50*4*60
        self.ema_period_15m_eth = 50*15
        # Parametrii generali
        self.stop_loss_pct = 1
        self.take_profit_pct = 3
        self.rolling_window_size = 31
        # Parametrii pentru API Binance
        self.api_key = "YOUR_BINANCE_API_KEY"
        self.api_secret = "YOUR_BINANCE_API_SECRET"
        # Parametrii pentru gestionarea monedelor
        self.top_coins_to_monitor = 10
        self.constant_monitoring_coins = 5
        self.periodic_monitoring_coins = 5
        # Parametrii pentru optimizarea strategiei
        self.backtest_start_date = "YYYY-MM-DD"
        self.backtest_end_date = "YYYY-MM-DD"
        # Parametrii pentru tranzacționare cu levier
        self.leverage_level = 1  # 1 înseamnă fără levier
        # Parametrii pentru optimizare automată (opțional)
        self.auto_optimization = False
        # Parametrii pentru testare și implementare
        self.testnet = True  # Dacă este True, botul va rula pe Binance Testnet
