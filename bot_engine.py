import time
import random

class TradingBot:

    def __init__(self):
        self.balance = 10000
        self.positions = []
        self.pnl = 0
        self.running = True

    def get_market_signal(self):
        # Simulación IA (luego pondremos la real)
        return random.choice(["buy", "sell", "hold"])

    def execute_trade(self, signal):
        if signal == "buy":
            amount = random.randint(50, 200)
            self.positions.append(amount)
            print(f"Compra simulada: {amount}")

        elif signal == "sell" and self.positions:
            amount = self.positions.pop()
            profit = random.randint(-20, 50)
            self.pnl += profit
            print(f"Venta simulada: {amount} | PnL: {profit}")

    def run(self):
        print("Bot iniciado...")
        while self.running:
            signal = self.get_market_signal()
            self.execute_trade(signal)
            time.sleep(5)

    def stop(self):
        self.running = False


bot = TradingBot()
