import telebot
import os
from telebot import types

TOKEN = os.getenv("BOT_TOKEN", "8808674212:AAGNVTDdsNYKA6SMu5c3q2kx_3x1VnmIrjM")
PHONE = "992018556060"

bot = telebot.TeleBot(TOKEN)

PRICES = {
    "d110": ("💎 100+10=110", "9,45 смн"),
    "d341": ("💎 310+31=341", "28,70 смн"),
    "d572": ("💎 520+52=572", "45,20 смн"),
    "d1166": ("💎 1060+106=1166", "85,55 смн"),
    "d2398": ("🎁 2180+218=2398", "171,10 смн"),
    "d6160": ("💰 5600+560=6160", "437,10 смн"),
    "v_lite": ("🎟️ Ваучер Lite 90 (7д)", "4,75 смн"),
    "v_week": ("🎟️ Ваучер Неделя 450", "17,85 смн"),
    "v_month": ("👑 Ваучер Месяц 2600", "63,50 смн"),
    "l6": ("⭐ Уровень 6", "3,80 смн"),
    "l10": ("⭐ Уровень 10", "6,75 смн"),
    "l15": ("⭐ Уровень 15", "6,75 смн"),
    "l20": ("⭐ Уровень 20", "6,75 смн"),
    "l25": ("⭐ Уровень 25", "6,75 смн"),
    "l30": ("⭐ Уровень 30", "9,35 смн"),
}

@bot.message_handler(commands=['start'])
def start(m):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for key, (name, price) in PRICES.items():
        markup.add(types.InlineKeyboardButton(f"{name} - {price}", callback_data=key))
    markup.add(types.InlineKeyboardButton("🌐 Сайт", url="https://almaz-shop.onrender.com"))
    markup.add(types.InlineKeyboardButton("📲 WhatsApp", url=f"https://wa.me/{PHONE}"))
    text = "💎 *ALMAZ SHOP - FREE FIRE TJ* 💎\n\nАрзонтарин алмазҳо!\n👇 Интихоб кун:"
    bot.send_message(m.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data in PRICES:
        name, price = PRICES[call.data]
        msg = bot.send_message(call.message.chat.id, f"✅ {name} - {price}\n\n🆔 ID Free Fire-и худро нависед:")
        bot.register_next_step_handler(msg, lambda m: get_id(m, name, price))

def get_id(m, name, price):
    uid = m.text
    msg = bot.send_message(m.chat.id, "👤 Ном (ё /skip):")
    bot.register_next_step_handler(msg, lambda n: finalize(n, name, price, uid))

def finalize(m, name, price, uid):
    user_name = m.text if m.text != "/skip" else ""
    bot.send_message(m.chat.id, f"✅ Қабул шуд!\n🎮 {name}\n💰 {price}\n🆔 {uid}\n\n📲 Барои пардохт: +992 018 556 060 WhatsApp")
    print(f"ORDER: {name} | {price} | ID:{uid}")

bot.infinity_polling()
