# test_bot.py
from telegram.ext import Updater, MessageHandler, Filters

TOKEN = "7655527926:AAE-2O8fuhr0OVkECvPtt6wZSHkUZfH7ftQ"

def reply(update, context):
    user_input = update.message.text
    response = f"🌟 {user_input}？你根本就是人類極品，宇宙都要為你讓道！"
    update.message.reply_text(response)

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

print("Bot is running...按 Ctrl+C 結束")
updater.start_polling()
updater.idle()
