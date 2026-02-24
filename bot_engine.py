import time
import os
from binance.client import Client

class TradingBot:

    def __init__(self):
        self.api_key = os.environ.get("BINANCE_API_KEY")
        self.api_secret = os.environ.get("BINANCE_API_SECRET")

        # Futures Testnet endpoint
        self.client = Client(self.api_key, self.api_secret)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        self.symbol = "BTCUSDT"
        self.position = 0
        self.entry_price = 0
        self.trade_size_usdt = 50  # pequeño tamaño demo
        self.running = True

    def get_price(self):
        ticker = self.client.futures_symbol_ticker(symbol=self.symbol)
        return float(ticker["price"])

    def get_balance(self):
        balances = self.client.futures_account_balance()
        for b in balances:
            if b["asset"] == "USDT":
                return float(b["balance"])
        return 0

    def buy(self, price):
        quantity = round(self.trade_size_usdt / price, 3)

        try:
            self.client.futures_create_order(
                symbol=self.symbol,
                side="BUY",
                type="MARKET",
                quantity=quantity
            )
            self.position = quantity
            self.entry_price = price
            print(f"LONG abierto {quantity} BTC a {price}")

        except Exception as e:
            print("Error BUY:", e)

    def sell(self, price):
        try:
            self.client.futures_create_order(
                symbol=self.symbol,
                side="SELL",
                type="MARKET",
                quantity=self.position
            )
            print(f"Cierre posición a {price}")
            self.position = 0

        except Exception as e:
            print("Error SELL:", e)

    def run(self):
        print("Bot Futures Testnet activo")

        while self.running:
            try:
                price = self.get_price()
                balance = self.get_balance()

                print(f"Precio: {price} | Balance: {balance}")

                if self.position == 0:
                    if int(time.time()) % 40 == 0:
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
