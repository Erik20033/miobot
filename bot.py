import telebot
from flask import Flask
from threading import Thread
import os

# --- SERVER PER TENERLO SVEGLIO (RENDER/KOYEB) ---
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

# Dizionario temporaneo per memorizzare l'ultimo messaggio di avviso inviato a ogni utente
# Formato: {user_id: message_id_del_bot}
pending_warnings = {}

@bot.message_handler(func=lambda m: True)
def check_membership(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Salta il controllo per gli admin del gruppo
    try:
        if bot.get_chat_member(chat_id, user_id).status in ['administrator', 'creator']:
            return
    except:
        pass

    try:
        # Controllo iscrizione al canale
        member = bot.get_chat_member(CH_USERNAME, user_id)
        is_member = member.status in ['member', 'administrator', 'creator']

        if not is_member:
            # 1. CANCELLA IL MESSAGGIO DELL'UTENTE
            bot.delete_message(chat_id, message.message_id)

            # 2. CANCELLA IL VECCHIO AVVISO SE ESISTE (PULIZIA CHAT)
            if user_id in pending_warnings:
                try:
                    bot.delete_message(chat_id, pending_warnings[user_id])
                except:
                    pass # Se è già stato cancellato manualmente, ignora l'errore

            # 3. MANDA IL NUOVO AVVISO E SALVA L'ID
            new_msg = bot.send_message(
                chat_id, 
                f"⚠️ Ehi {message.from_user.first_name}, per scrivere qui devi prima unirti al canale {CH_USERNAME}!"
            )
            pending_warnings[user_id] = new_msg.message_id

        else:
            # SE L'UTENTE È ISCRITTO: cancella l'ultimo avviso del bot (se presente) e lascialo scrivere
            if user_id in pending_warnings:
                try:
                    bot.delete_message(chat_id, pending_warnings[user_id])
                    del pending_warnings[user_id] # Pulisce la memoria
                except:
                    pass

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    Thread(target=run).start()
    print("Bot con pulizia messaggi attivo!")
    bot.infinity_polling()
