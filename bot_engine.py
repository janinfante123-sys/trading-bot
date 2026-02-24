import time
import os
from binance.client import Client

class TradingBot:

    def __init__(self):
        self.api_key = os.environ.get("BINANCE_API_KEY")
        self.api_secret = os.environ.get("BINANCE_API_SECRET")

        self.client = Client(self.api_key, self.api_secret)
        self.client.API_URL = 'https://testnet.binance.vision/api'

        self.symbol = "BTCUSDT"
        self.trade_size = 5  # USDT por operación (demo)
        self.position = None
        self.entry_price = 0
        self.running = True

    def get_price(self):
        ticker = self.client.get_symbol_ticker(symbol=self.symbol)
        return float(ticker["price"])

    def buy(self, price):
        quantity = round(self.trade_size / price, 5)
        order = self.client.create_order(
            symbol=self.symbol,
            side="BUY",
            type="MARKET",
            quantity=quantity
        )
        self.position = quantity
        self.entry_price = price
        print(f"Compra {quantity} BTC a {price}")

    def sell(self, price):
        order = self.client.create_order(
            symbol=self.symbol,
            side="SELL",
            type="MARKET",
            quantity=self.position
        )
        profit = (price - self.entry_price) * self.position
        print(f"Venta a {price} | Profit: {profit}")
        self.position = None

    def run(self):
        print("Bot trading demo activo")
        while self.running:
            price = self.get_price()
            print("Precio:", price)

            if self.position is None:
                # señal simple de compra
                if int(time.time()) % 60 == 0:
                    self.buy(price)

            else:
                # take profit demo
                if price > self.entry_price * 1.002:
                    self.sell(price)

                # stop loss demo
                if price < self.entry_price * 0.998:
                    self.sell(price)

            time.sleep(5)

    def stop(self):
        self.running = False


bot = TradingBot()
