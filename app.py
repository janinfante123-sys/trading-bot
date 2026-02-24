from flask import Flask, jsonify
from threading import Thread
import bot_engine

app = Flask(__name__)
bot = bot_engine.bot

def start_bot():
    bot.run()

@app.route("/")
def home():
    return "Bot activo 🚀"

@app.route("/status")
def status():
    try:
        return jsonify({
            "balance": getattr(bot, "balance", 0),
            "position": getattr(bot, "position", 0),
            "entry_price": getattr(bot, "entry_price", 0),
            "running": bot.running
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/start")
def start():
    if not bot.running:
        bot.running = True
        Thread(target=start_bot).start()
    return "Bot iniciado"

@app.route("/stop")
def stop():
    bot.stop()
    return "Bot detenido"

if __name__ == "__main__":
    Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=10000)
