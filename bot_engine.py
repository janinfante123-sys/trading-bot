import time
import os
from binance.client import Client

class TradingBot:

    def __init__(self):
        self.api_key = os.environ.get("BINANCE_API_KEY")
        self.api_secret = os.environ.get("BINANCE_API_SECRET")

        # conexión a Binance TESTNET
        self.client = Client(self.api_key, self.api_secret)
        self.client.API_URL = 'https://testnet.binance.vision/api'

        self.balance = 0
        self.positions = []
        self.pnl = 0
        self.running = True

    def update_balance(self):
        try:
            account = self.client.get_account()
            for asset in account["balances"]:
                if asset["asset"] == "USDT":
                    self.balance = float(asset["free"])
        except Exception as e:
            print("Error balance:", e)

    def get_price(self, symbol="BTCUSDT"):
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker["price"])
        except:
            return None

    def run(self):
        print("Bot conectado a Binance Testnet")
        while self.running:
            self.update_balance()
            price = self.get_price()

            if price:
                print(f"Precio BTC: {price} | Balance: {self.balance}")

            time.sleep(10)

    def stop(self):
        self.running = False


bot = TradingBot()
