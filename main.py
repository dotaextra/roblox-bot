import requests
from telegram.ext import ApplicationBuilder, ContextTypes
# УБРАНО: from keep_alive import keep_alive

# --- НАСТРОЙКИ ---
BOT_TOKEN = "9176970614:AAHFOqZIh_GOMojON-BbH_bQC5bNVEOStKk"
CHAT_ID = 362678203 
ROBLOX_USER_IDS = [7821605292, 8500408550]
CHECK_INTERVAL = 60

previous_statuses = {}

def get_roblox_status(user_ids):
    url = "https://presence.roblox.com/v1/presence/users"
    payload = {"userIds": user_ids}
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        statuses = {}
        for user in data.get('userPresences', []):
            uid = user['userId']
            status_map = {0: "Оффлайн", 1: "Онлайн (в меню)", 2: "В игре"}
            statuses[uid] = status_map.get(user['userPresenceType'], "Неизвестно")
        return statuses
    except Exception as e:
        print(f"Ошибка Roblox: {e}")
        return {}

async def check_and_notify(context: ContextTypes.DEFAULT_TYPE):
    current_statuses = get_roblox_status(ROBLOX_USER_IDS)
    for uid, status in current_statuses.items():
        prev_status = previous_statuses.get(uid)
        if prev_status != status:
            message = f"🎮 Roblox Alert:\nUser ID: {uid}\nСтатус: {status}"
            try:
                await context.bot.send_message(chat_id=CHAT_ID, text=message)
                print(f"Отправлено: {uid} - {status}")
            except Exception as e:
                print(f"Ошибка Telegram: {e}")
            previous_statuses[uid] = status

if __name__ == '__main__':
    # УБРАНО: keep_alive()
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    job_queue = application.job_queue
    job_queue.run_repeating(check_and_notify, interval=CHECK_INTERVAL, first=5)
    
    print("✅ Бот запущен и следит за Roblox!")
    application.run_polling(drop_pending_updates=True)
