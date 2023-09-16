import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class PerformanceAnalysis:

    def __init__(self, returns):
        self.returns = returns

    def total_return(self):
        return np.prod(1 + self.returns) - 1

    def mean_return(self):
        return np.mean(self.returns)

    def volatility(self):
        return np.std(self.returns)

    def max_drawdown(self):
        cumulative_returns = (1 + self.returns).cumprod()
        max_return = cumulative_returns.expanding().max()
        drawdown = cumulative_returns / max_return - 1
        return drawdown.min()

    def sharpe_ratio(self, risk_free_rate=0.02):
        excess_return = self.mean_return() - risk_free_rate
        return excess_return / self.volatility()

    def trade_analysis(self, trades):
        total_trades = len(trades)
        profitable_trades = sum(1 for trade in trades if trade > 0)
        return {
            "Total Trades": total_trades,
            "Profitable Trades": profitable_trades,
            "Winning Percentage": profitable_trades / total_trades,
            "Average Win": np.mean([trade for trade in trades if trade > 0]),
            "Average Loss": np.mean([trade for trade in trades if trade < 0])
        }

    def profit_loss_distribution(self, trades):
        plt.hist(trades, bins=20, alpha=0.75)
        plt.title("Profit and Loss Distribution")
        plt.xlabel("Returns")
        plt.ylabel("Frequency")
        plt.show()

    def correlation_with_benchmark(self, benchmark_returns):
        return np.corrcoef(self.returns, benchmark_returns)[0, 1]

# Puteți utiliza această clasă astfel:
# analysis = PerformanceAnalysis(returns)
# print("Total Return:", analysis.total_return())
# ... și așa mai departe pentru celelalte funcții.
