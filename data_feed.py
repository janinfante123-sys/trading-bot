import requests
import yfinance as yf

def get_crypto():
    r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
    btc = float(r.json()["price"])

    r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
    eth = float(r.json()["price"])

    return {
        "BTCUSDT": btc,
        "ETHUSDT": eth
    }

def get_forex():
    r = requests.get("https://api.exchangerate.host/latest?base=EUR&symbols=USD")
    eurusd = r.json()["rates"]["USD"]
    return {"EURUSD": eurusd}

def get_stocks():
    aapl = yf.Ticker("AAPL").history(period="1d")["Close"].iloc[-1]
    tsla = yf.Ticker("TSLA").history(period="1d")["Close"].iloc[-1]
    return {"AAPL": aapl, "TSLA": tsla}

def get_all_prices():
    prices = {}
    prices.update(get_crypto())
    prices.update(get_forex())
    prices.update(get_stocks())
    return prices
