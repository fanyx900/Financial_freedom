class TradeManager:
    def __init__(self, algo):
        self.algo = algo

    def place_buy_order(self, symbol, quantity, stop_loss_pct, take_profit_pct):
        # Plasare ordin de cumpărare
        self.algo.SetHoldings(symbol, quantity)
        
        # Calculare prețuri pentru stop loss și take profit
        current_price = self.algo.Securities[symbol].Price
        stop_price = round(current_price * (1 - stop_loss_pct / 100), 2)
        limit_price = round(current_price * (1 + take_profit_pct / 100), 2)
        
        # Plasare ordine stop loss și take profit
        self.algo.StopMarketOrder(symbol, -self.algo.Portfolio[symbol].Quantity, stop_price)
        self.algo.LimitOrder(symbol, -self.algo.Portfolio[symbol].Quantity, limit_price)

    def place_sell_order(self, symbol):
        # Plasare ordin de vânzare
        self.algo.SetHoldings(symbol, 0)

    def place_short_order(self, symbol, quantity, stop_loss_pct, take_profit_pct):
        # Plasare ordin de vânzare în scurt
        self.algo.SetHoldings(symbol, -quantity)
        
        # Calculare prețuri pentru stop loss și take profit
        current_price = self.algo.Securities[symbol].Price
        stop_price = round(current_price * (1 + stop_loss_pct / 100), 2)
        limit_price = round(current_price * (1 - take_profit_pct / 100), 2)
        
        # Plasare ordine stop loss și take profit
        self.algo.StopMarketOrder(symbol, self.algo.Portfolio[symbol].Quantity, stop_price)
        self.algo.LimitOrder(symbol, self.algo.Portfolio[symbol].Quantity, limit_price)

    def close_position(self, symbol):
        # Închidere poziție
        self.algo.Liquidate(symbol)
        