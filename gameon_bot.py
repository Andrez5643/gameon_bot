import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

ADMIN_USERNAME = "@KaliDapper"

def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("💸 Deposit"),
        KeyboardButton("🏦 Withdraw")
    )
    markup.add(
        KeyboardButton("📊 Balance"),
        KeyboardButton("🧾 How to Deposit"),
        KeyboardButton("🆘 Support")
    )
    bot.send_message(
        chat_id,
        "🎰 Welcome to *GameOn!*\n\nChoose an option below to:\n• 💸 Make a Deposit\n• 💵 Request a Payout\n• 📊 Check Balance\n• 🧾 Learn How to Deposit\n• 🆘 Contact Support",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["start"])
def start(message):
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() in ["💸 deposit", "deposit"])
def deposit(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("CashApp"),
        KeyboardButton("Apple Pay"),
        KeyboardButton("Venmo"),
        KeyboardButton("Crypto")
    )
    bot.send_message(message.chat.id, "Choose your deposit method:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() == "cashapp")
def cashapp(message):
    bot.send_message(message.chat.id, "💵 Send payment via *CashApp* to `$myposhsolutions` and reply with a screenshot.", parse_mode="Markdown")
    bot.send_message(ADMIN_USERNAME, f"📨 {message.from_user.first_name} selected CashApp to deposit.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() == "apple pay")
def applepay(message):
    bot.send_message(message.chat.id, "📱 Send payment via *Apple Pay* to `346-475-8302` and reply with a screenshot.", parse_mode="Markdown")
    bot.send_message(ADMIN_USERNAME, f"📨 {message.from_user.first_name} selected Apple Pay to deposit.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() == "venmo")
def venmo(message):
    bot.send_message(message.chat.id, "💳 Send payment via *Venmo* to `@drellanno` and reply with a screenshot.", parse_mode="Markdown")
    bot.send_message(ADMIN_USERNAME, f"📨 {message.from_user.first_name} selected Venmo to deposit.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() == "crypto")
def crypto(message):
    crypto_info = (
        "🪙 *Choose a crypto and send funds to the address below:*\n\n"
        "*DOGE:* `D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98`\n"
        "*SOL:* `2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA`\n"
        "*ETH:* `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
        "*USDT (Avalanche C):* `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
        "*XRP (BNB Beacon):* `bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2`\n\n"
        "📩 *Reply here with the transaction screenshot and crypto used.*"
    )
    bot.send_message(message.chat.id, crypto_info, parse_mode="Markdown")
    bot.send_message(ADMIN_USERNAME, f"📨 {message.from_user.first_name} selected Crypto to deposit.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() == "📊 balance")
def balance(message):
    bot.send_message(message.chat.id, "📊 Balance feature coming soon!")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() == "🧾 how to deposit")
def how_to_deposit(message):
    bot.send_message(message.chat.id, "🧾 To deposit, select a method and send the payment. Then reply with your screenshot.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() == "🆘 support")
def support(message):
    bot.send_message(message.chat.id, f"📞 For support, contact {ADMIN_USERNAME}")

bot.infinity_polling()




