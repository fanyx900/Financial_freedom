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
