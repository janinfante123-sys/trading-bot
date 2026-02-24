import time

class PortfolioEngine:

    def __init__(self):
        self.balance = 10000
        self.positions = {}
        self.trades = []
        self.equity_curve = []

        self.assets = {
            "BTCUSDT": {"type":"crypto"},
            "ETHUSDT": {"type":"crypto"},
            "EURUSD": {"type":"forex"},
            "AAPL": {"type":"stock"},
            "TSLA": {"type":"stock"}
        }

        self.risk_per_trade = 0.02

    def open_position(self, symbol, price):
        if symbol not in self.positions:
            size = self.balance * self.risk_per_trade
            qty = size / price
            self.positions[symbol] = {
                "entry": price,
                "qty": qty
            }

    def close_position(self, symbol, price):
        if symbol in self.positions:
            pos = self.positions[symbol]
            pnl = (price - pos["entry"]) * pos["qty"]
            self.balance += pnl

            self.trades.append({
                "symbol": symbol,
                "entry": pos["entry"],
                "exit": price,
                "pnl": pnl
            })

            del self.positions[symbol]

    def step(self, prices):
        for symbol, price in prices.items():

            if symbol not in self.positions:
                if time.time() % 30 < 2:
                    self.open_position(symbol, price)

            else:
                entry = self.positions[symbol]["entry"]

                if price > entry * 1.01 or price < entry * 0.99:
                    self.close_position(symbol, price)

        self.equity_curve.append(self.balance)

    def get_status(self):
        return {
            "balance": round(self.balance,2),
            "positions": self.positions,
            "trades": self.trades[-20:],
            "equity": self.equity_curve[-200:]
        }

engine = PortfolioEngine()
