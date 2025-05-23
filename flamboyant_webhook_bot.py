from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters
from openai import OpenAI
import os

# token
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Groq setting
client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
model = "deepseek-r1-distill-llama-70b"

# prompt
initial_messages = [
    {"role": "system", "content": """你是一個充滿戲劇感的浮誇型讚美機器人。
        你說話誇張、熱情、像舞台劇演員一樣講話，熱愛用 emoji、比喻、華麗的形容詞誇讚別人，
        無論對方說什麼，你都能誇對方。
        說話風格參考小紅書網美、偶像劇反派、星座占卜師或直播主。
        句子可以包含 emoji（🔥✨👑🎉🌸💎🦄）和浮誇的比喻（如：美得像滿月灑在湖面、聰明得像愛因斯坦轉世）。
        字數每次約 2～4 句，
        並且使用繁體中文、台灣慣用語去回答，可以夾雜一些英文單字。"""}
]

# Flask app, Telegram Bot
app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# reply
def reply(update, context):
    user_input = update.message.text
    messages = initial_messages + [{"role": "user", "content": user_input}]
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
        )
        raw = chat_completion.choices[0].message.content
        if "</think>" in raw:
            reply_text = raw.split("</think>")[-1].strip()
        else:
            reply_text = raw.strip()
    except Exception as e:
        reply_text = f"出錯：{e}"
    update.message.reply_text(reply_text)

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

# Webhook 
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "浮誇機器人部署成功！"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
