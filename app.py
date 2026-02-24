from flask import Flask, render_template, jsonify
import threading
import time
from engine import engine
from data_feed import get_all_prices

app = Flask(__name__)

def loop():
    while True:
        prices = get_all_prices()
        engine.step(prices)
        time.sleep(5)

threading.Thread(target=loop, daemon=True).start()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/data")
def data():
    return jsonify(engine.get_status())

if __name__ == "__main__":
    app.run()
