import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_USERNAME = "@GameOnHost"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("💸 Deposit"),
        KeyboardButton("🏦 Withdraw")
    )
    markup.add(
        KeyboardButton("📊 Balance"),
        KeyboardButton("🧾 How to Deposit")
    )
    markup.add(
        KeyboardButton("🆘 Support")
    )
    bot.send_message(
        chat_id,
        "🎰 Welcome to *GameOn*, where the odds work in your favor! 💸

"
        "We're more than just a sportsbook — we're your personal line to big wins, fast payouts, and premium support. ✅

"
        "🏆 What to expect:
"
        "• 💵 Easy Deposits (CashApp, Venmo, Apple Pay, Crypto)
"
        "• 🏦 Fast Withdrawals — every Tuesday
"
        "• 🎁 Exclusive Bonuses & Free Plays
"
        "• 🧠 Real Humans, Real Help

"
        "Your next win starts here. If you ever need support, tap 🆘 or message @GameOnHost.

"
        "💬 Hit \"💸 Deposit\" to get started!",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["start"])
def start(message):
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda msg: msg.text == "💸 Deposit")
def deposit(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("CashApp"), KeyboardButton("Apple Pay"))
    markup.add(KeyboardButton("Venmo"), KeyboardButton("Crypto"))
    markup.add(KeyboardButton("⬅️ Back"))
    bot.send_message(message.chat.id, "Select your deposit method:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "CashApp")
def cashapp(message):
    bot.send_message(message.chat.id, "💵 Send payment via *CashApp* to `$myposhsolutions` and reply with a screenshot.", parse_mode="Markdown")
    bot.send_message(ADMIN_USERNAME, f"📨 {message.from_user.first_name} selected CashApp to deposit.")

@bot.message_handler(func=lambda msg: msg.text == "Apple Pay")
def applepay(message):
    bot.send_message(message.chat.id, "📱 Send payment via *Apple Pay* to `346-475-8302` and reply with a screenshot.", parse_mode="Markdown")
    bot.send_message(ADMIN_USERNAME, f"📨 {message.from_user.first_name} selected Apple Pay to deposit.")

@bot.message_handler(func=lambda msg: msg.text == "Venmo")
def venmo(message):
    bot.send_message(message.chat.id, "💳 Send payment via *Venmo* to `@drellanno` and reply with a screenshot.", parse_mode="Markdown")
    bot.send_message(ADMIN_USERNAME, f"📨 {message.from_user.first_name} selected Venmo to deposit.")

@bot.message_handler(func=lambda msg: msg.text == "Crypto")
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

@bot.message_handler(func=lambda msg: msg.text == "🏦 Withdraw")
def withdraw(message):
    bot.send_message(message.chat.id, f"🏦 To request a payout, please message {ADMIN_USERNAME} directly.")

@bot.message_handler(func=lambda msg: msg.text == "📊 Balance")
def balance(message):
    bot.send_message(message.chat.id, f"📊 Balance updates are handled manually. Message {ADMIN_USERNAME} to request your balance.")

@bot.message_handler(func=lambda msg: msg.text == "🧾 How to Deposit")
def how_to_deposit(message):
    bot.send_message(message.chat.id, "🧾 Steps to deposit:\n\n1. Tap 💸 Deposit\n2. Select your payment method\n3. Send payment\n4. Reply with a screenshot")

@bot.message_handler(func=lambda msg: msg.text == "🆘 Support")
def support(message):
    bot.send_message(message.chat.id, f"📞 For help, message {ADMIN_USERNAME}")

@bot.message_handler(func=lambda msg: msg.text == "⬅️ Back")
def back(message):
    show_main_menu(message.chat.id)

bot.infinity_polling()




