from telegram.ext import Updater, MessageHandler, Filters
from openai import OpenAI

# === 請填入你的 Token ===
TELEGRAM_TOKEN = "7655527926:AAE-2O8fuhr0OVkECvPtt6wZSHkUZfH7ftQ"
GROQ_API_KEY = "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"

# === Groq 設定 ===
client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
model = "deepseek-r1-distill-llama-70b"

# === 浮誇風格初始 prompt ===
initial_messages = [
    {"role": "system", "content": """你是一個充滿戲劇感的浮誇型讚美機器人。
你說話誇張、熱情、像舞台劇演員一樣講話，熱愛用 emoji、比喻、華麗的形容詞誇讚別人，
無論對方說了什麼，你都能用浮誇方式找到值得稱讚的地方。
說話風格參考小紅書網美、偶像劇反派、星座占卜師或直播主。
句子可以包含 emoji（🔥✨👑🎉🌸💎🦄）和浮誇的比喻（如：美得像滿月灑在湖面、聰明得像愛因斯坦轉世）。
字數每次約 2～4 句，熱情澎湃但不要太冗長。
並且使用繁體中文、台灣慣用語去回答，如果要夾雜非繁體中文的語言，請用英文。"""}
]

# === Telegram 回應邏輯 ===
def reply(update, context):
    user_input = update.message.text
    messages = initial_messages + [{"role": "user", "content": user_input}]
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
        )
        raw_reply = chat_completion.choices[0].message.content
        if "</think>" in raw_reply:
            reply_text = raw_reply.split("</think>")[-1].strip()
        else:
            reply_text = raw_reply.strip()
    except Exception as e:
        reply_text = "⚠️ 發生錯誤啦～請稍後再試！（錯誤訊息：" + str(e) + "）"
    update.message.reply_text(reply_text)

# === 啟動 Bot ===
updater = Updater(TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

print("🌟 浮誇讚美機器人正在運作中！請打開 Telegram 和它對話！")
updater.start_polling()
updater.idle()
