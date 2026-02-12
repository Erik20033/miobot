import telebot
from flask import Flask
from threading import Thread
import os

# --- SERVER PER TENERLO SVEGLIO ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

# --- CONFIGURAZIONE BOT ---
TOKEN = '8502522551:AAFB5vy8ynwHffEXKFv2gZ86aJLQILOMQBc'
CH_USERNAME = '@bullbonusitalia'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def check_membership(message):
    try:
        status = bot.get_chat_member(CH_USERNAME, message.from_user.id).status
        if status in ['left', 'kicked']:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, f"⚠️ Unisciti a {CH_USERNAME} per scrivere!")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    Thread(target=run).start() # Avvia il server finto
    print("Bot partito!")
    bot.infinity_polling()
