from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Бот работает! 🤖"

def run():
    # Запускаем сервер на порту 8080 (стандарт для Render)
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()