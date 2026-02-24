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
        self.trade_size = 5  # USDT
        self.position = 0
        self.entry_price = 0
        self.running = True

    def get_price(self):
        ticker = self.client.get_symbol_ticker(symbol=self.symbol)
        return float(ticker["price"])

    def buy(self, price):
        quantity = round(self.trade_size / price, 6)

        try:
            order = self.client.create_order(
                symbol=self.symbol,
                side="BUY",
                type="MARKET",
                quantity=quantity
            )
            self.position = quantity
            self.entry_price = price
            print(f"Compra {quantity} BTC a {price}")

        except Exception as e:
            print("Error BUY:", e)

    def sell(self, price):
        try:
            order = self.client.create_order(
                symbol=self.symbol,
                side="SELL",
                type="MARKET",
                quantity=self.position
            )
            print("Venta ejecutada")
            self.position = 0

        except Exception as e:
            print("Error SELL:", e)

    def run(self):
        print("Bot trading demo activo")

        while self.running:
            try:
                price = self.get_price()
                print("Precio:", price)

                if self.position == 0:
                    if int(time.time()) % 30 == 0:
                        self.buy(price)

                else:
                    if price > self.entry_price * 1.002:
                        self.sell(price)

                    if price < self.entry_price * 0.998:
                        self.sell(price)

                time.sleep(5)

            except Exception as e:
                print("Loop error:", e)
                time.sleep(5)

    def stop(self):
        self.running = False


bot = TradingBot()
