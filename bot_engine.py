import time
import os
from binance.client import Client

class TradingBot:

    def __init__(self):
        self.api_key = os.environ.get("BINANCE_API_KEY")
        self.api_secret = os.environ.get("BINANCE_API_SECRET")

        self.client = Client(self.api_key, self.api_secret)
        
        # ENDPOINT CORRECTO FUTURES TESTNET
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        self.symbol = "BTCUSDT"
        self.position = 0
        self.entry_price = 0
        self.trade_size_usdt = 25
        self.running = True

    def get_price(self):
        ticker = self.client.futures_symbol_ticker(symbol=self.symbol)
        return float(ticker["price"])

    def get_balance(self):
        acc = self.client.futures_account_balance()
        for a in acc:
            if a["asset"] == "USDT":
                return float(a["balance"])
        return 0

    def buy(self, price):
        qty = round(self.trade_size_usdt / price, 3)
        try:
            self.client.futures_create_order(
                symbol=self.symbol,
                side="BUY",
                type="MARKET",
                quantity=qty
            )
            self.position = qty
            self.entry_price = price
            print("LONG abierta")
        except Exception as e:
            print("BUY error:", e)

    def sell(self, price):
        try:
            self.client.futures_create_order(
                symbol=self.symbol,
                side="SELL",
                type="MARKET",
                quantity=self.position
            )
            print("Posición cerrada")
            self.position = 0
        except Exception as e:
            print("SELL error:", e)

    def run(self):
        print("Bot futures testnet activo")

        while self.running:
            try:
                price = self.get_price()
                balance = self.get_balance()
                print("Balance:", balance)

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
