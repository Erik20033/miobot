import telebot
from flask import Flask
from threading import Thread

# Server per tenere sveglio il bot su Render
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"

def run(): app.run(host='0.0.0.0', port=8080)

TOKEN = '8502522551:AAFB5vy8ynwHffEXKFv2gZ86aJLQILOMQBc'
CH_USERNAME = '@bullbonusitalia'
bot = telebot.TeleBot(TOKEN)

# Memoria per i messaggi di avviso
pending_alerts = {}

@bot.message_handler(func=lambda m: True, content_types=['text', 'photo', 'video', 'sticker', 'animation', 'document'])
def check_and_clean(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # 1. Saltiamo gli admin
    try:
        if bot.get_chat_member(chat_id, user_id).status in ['administrator', 'creator']:
            return
    except: pass

    # 2. Controllo Iscrizione
    try:
        status = bot.get_chat_member(CH_USERNAME, user_id).status
        is_member = status in ['member', 'administrator', 'creator']

        if not is_member:
            # UTENTE NON ISCRITTO: Cancella quello che ha scritto
            bot.delete_message(chat_id, message.message_id)

            # Cancella il vecchio avviso (se esisteva già) per non intasare
            if user_id in pending_alerts:
                try: bot.delete_message(chat_id, pending_alerts[user_id])
                except: pass

            # Manda il nuovo avviso
            sent_msg = bot.send_message(chat_id, f"⚠️ Benvenuto {message.from_user.first_name}, devi unirti al canale {CH_USERNAME} prima di poter scrivere qui!")
            pending_alerts[user_id] = sent_msg.message_id

        else:
            # UTENTE ISCRITTO: Se c'è un avviso vecchio, cancellalo ora che ha scritto da iscritto
            if user_id in pending_alerts:
                try:
                    bot.delete_message(chat_id, pending_alerts[user_id])
                    del pending_alerts[user_id]
                except: pass

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling(allowed_updates=['message', 'chat_member'])
