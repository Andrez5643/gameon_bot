import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
ADMIN_USERNAME = "@KaliDapper"

# Main menu layout
def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("💸 Deposit"), KeyboardButton("🏦 Withdraw"))
    markup.add(KeyboardButton("📊 Balance"), KeyboardButton("🧾 How to Deposit"))
    markup.add(KeyboardButton("🆘 Support"))

    bot.send_message(
        chat_id,
        "🎰 Welcome to *GameOn!*\n\nChoose an option below to:\n\n"
        "💸 *Deposit*\n"
        "🏦 *Withdraw*\n"
        "📊 *Balance*\n"
        "🧾 *How to Deposit*\n"
        "🆘 *Support*",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# Start command
@bot.message_handler(commands=["start"])
def start(message):
    show_main_menu(message.chat.id)

# Deposit flow
@bot.message_handler(func=lambda msg: msg.text.lower() in ["💸 deposit", "deposit"])
def deposit(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("CashApp"), KeyboardButton("Apple Pay"))
    markup.add(KeyboardButton("Venmo"), KeyboardButton("Crypto"))
    markup.add(KeyboardButton("⬅️ Back"))
    bot.send_message(message.chat.id, "Select your deposit method below:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text.lower() == "cashapp")
def cashapp(message):
    bot.send_message(message.chat.id, "💵 Send payment via *CashApp* to `$myposhsolutions` and reply with a screenshot.")
    bot.send_message(ADMIN_USERNAME, f"📨 {message.from_user.first_name} selected *CashApp* for deposit.")

@bot.message_handler(func=lambda msg: msg.text.lower() == "apple pay")
def applepay(message):
    bot.send_message(message.chat.id, "📱 Send payment via *Apple Pay* to `346-475-8302` and reply with a screenshot.")
    bot.send_message(ADMIN_USERNAME, f"📨 {message.from_user.first_name} selected *Apple Pay* for deposit.")

@bot.message_handler(func=lambda msg: msg.text.lower() == "venmo")
def venmo(message):
    bot.send_message(message.chat.id, "💳 Send payment via *Venmo* to `@drellanno` and reply with a screenshot.")
    bot.send_message(ADMIN_USERNAME, f"📨 {message.from_user.first_name} selected *Venmo* for deposit.")

@bot.message_handler(func=lambda msg: msg.text.lower() == "crypto")
def crypto(message):
    msg_text = (
        "🪙 *Crypto Deposit Instructions:*\n\n"
        "*DOGE:* `D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98`\n"
        "*SOL:* `2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA`\n"
        "*ETH:* `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
        "*USDT (Avalanche):* `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
        "*XRP (BNB Beacon):* `bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2`\n\n"
        "📸 Reply with your transaction screenshot once complete."
    )
    bot.send_message(message.chat.id, msg_text, parse_mode="Markdown")
    bot.send_message(ADMIN_USERNAME, f"📨 {message.from_user.first_name} selected *Crypto* for deposit.")

# Withdraw
@bot.message_handler(func=lambda msg: msg.text.lower() in ["🏦 withdraw", "withdraw", "cashout"])
def withdraw(message):
    bot.send_message(message.chat.id, f"🏦 To request a payout, please message {ADMIN_USERNAME} directly.")

# Balance
@bot.message_handler(func=lambda msg: msg.text.lower() in ["📊 balance", "balance"])
def balance(message):
    bot.send_message(message.chat.id, f"📊 Balance inquiries are handled manually. Please contact {ADMIN_USERNAME}.")

# How to Deposit
@bot.message_handler(func=lambda msg: msg.text.lower() in ["🧾 how to deposit", "how to deposit"])
def how_to_deposit(message):
    bot.send_message(message.chat.id, "🧾 To make a deposit:\n\n1. Tap 💸 Deposit\n2. Choose your method\n3. Send payment\n4. Reply with your screenshot\n\nYour account will be credited shortly after.")

# Support
@bot.message_handler(func=lambda msg: msg.text.lower() in ["🆘 support", "support"])
def support(message):
    bot.send_message(message.chat.id, f"🆘 For support, contact {ADMIN_USERNAME}")

# Back button
@bot.message_handler(func=lambda msg: msg.text.lower() in ["⬅️ back", "back"])
def back(message):
    show_main_menu(message.chat.id)

# Run the bot
bot.infinity_polling()




