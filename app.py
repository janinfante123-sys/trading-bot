from flask import Flask, jsonify
from threading import Thread
import bot_engine

app = Flask(__name__)

bot = bot_engine.bot

# Hilo para que el bot corra en segundo plano
def start_bot():
    bot.run()

@app.route("/")
def home():
    return "Bot de trading activo 🚀"

@app.route("/status")
def status():
    return jsonify({
        "balance": bot.balance,
        "pnl": bot.pnl,
        "open_positions": len(bot.positions),
        "running": bot.running
    })

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
