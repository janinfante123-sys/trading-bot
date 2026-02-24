import time
import os
import requests
import hmac
import hashlib

class TradingBot:

    def __init__(self):
        self.api_key = os.environ.get("BINANCE_API_KEY")
        self.api_secret = os.environ.get("BINANCE_API_SECRET")

        self.base_url = "https://demo.binance.com"
        self.symbol = "BTCUSDT"
        self.position = 0
        self.entry_price = 0
        self.trade_size_usdt = 50
        self.running = True

    def sign(self, params):
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()
        return query_string + "&signature=" + signature

    def get_balance(self):
        try:
            params = {
                "timestamp": int(time.time() * 1000)
            }
            query = self.sign(params)

            headers = {"X-MBX-APIKEY": self.api_key}

            response = requests.get(
                f"{self.base_url}/fapi/v2/balance?{query}",
                headers=headers
            )

            data = response.json()

            for asset in data:
                if asset["asset"] == "USDT":
                    return float(asset["balance"])

        except Exception as e:
            print("Balance error:", e)

        return 0

    def run(self):
        print("BOT CONECTADO A BINANCE DEMO DIRECTO")

        while self.running:
            balance = self.get_balance()
            print("Balance real:", balance)
            time.sleep(10)

    def stop(self):
        self.running = False


bot = TradingBot()
