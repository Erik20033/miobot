import telebot
from telebot.apihelper import ApiTelegramException

TOKEN = '8502522551:AAFB5vy8ynwHffEXKFv2gZ86aJLQILOMQBc'
CH_USERNAME = '@bullbonusitalia'

bot = telebot.TeleBot(TOKEN)

# Dizionario per ricordarsi i messaggi di avviso inviati (ID_UTENTE: ID_MESSAGGIO_BOT)
warned_users = {}

@bot.message_handler(func=lambda m: True)
def check_membership(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # 1. Saltiamo il controllo per gli admin
    try:
        if bot.get_chat_member(chat_id, user_id).status in ['administrator', 'creator']:
            return
    except:
        pass

    try:
        # 2. Controllo iscrizione al canale
        status = bot.get_chat_member(CH_USERNAME, user_id).status
        is_member = status in ['member', 'administrator', 'creator']

        if not is_member:
            # L'utente NON è iscritto: cancelliamo il suo messaggio
            bot.delete_message(chat_id, message.message_id)

            # Se avevamo già mandato un avviso, lo cancelliamo per non accumularli
            if user_id in warned_users:
                try:
                    bot.delete_message(chat_id, warned_users[user_id])
                except:
                    pass

            # Mandiamo il nuovo avviso e salviamo l'ID del messaggio
            msg = bot.send_message(
                chat_id, 
                f"⚠️ Ehi {message.from_user.first_name}, per scrivere qui devi prima unirti al canale {CH_USERNAME}!"
            )
            warned_users[user_id] = msg.message_id

        else:
            # L'utente È iscritto: se c'era un vecchio avviso, lo cancelliamo e puliamo il dizionario
            if user_id in warned_users:
                try:
                    bot.delete_message(chat_id, warned_users[user_id])
                except:
                    pass
                del warned_users[user_id]

    except ApiTelegramException as e:
        print(f"Errore API: {e}")

print("--- BOT AGGIORNATO: PULIZIA ATTIVA ---")
bot.infinity_polling()
