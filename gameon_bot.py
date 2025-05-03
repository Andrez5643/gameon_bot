import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USERNAME = "@KaliDapper"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💰 Deposit", "💸 Withdraw")
    markup.row("📊 Balance", "🧾 How to Deposit")
    markup.row("👤 Support")
    bot.send_message(message.chat.id, "👋 Welcome to GameOn! Please choose an option below:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "💰 Deposit")
def deposit_options(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("CashApp", callback_data="cashapp"))
    markup.add(types.InlineKeyboardButton("Apple Pay", callback_data="apple"))
    markup.add(types.InlineKeyboardButton("Venmo", callback_data="venmo"))
    markup.add(types.InlineKeyboardButton("Crypto", callback_data="crypto"))
    bot.send_message(message.chat.id, "Select a deposit method:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "💸 Withdraw")
def withdraw(message):
    bot.send_message(message.chat.id, "To request a payout, please message support at {}".format(ADMIN_USERNAME))

@bot.message_handler(func=lambda msg: msg.text == "📊 Balance")
def balance(message):
    bot.send_message(message.chat.id, "Balance inquiries are handled manually. Please message {}".format(ADMIN_USERNAME))

@bot.message_handler(func=lambda msg: msg.text == "🧾 How to Deposit")
def how_to_deposit(message):
    bot.send_message(message.chat.id, "To deposit, choose 💰 Deposit from the menu and follow instructions for your payment method.")

@bot.message_handler(func=lambda msg: msg.text == "👤 Support")
def support(message):
    bot.send_message(message.chat.id, "For support, please contact our agent: {}".format(ADMIN_USERNAME))

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    instructions = {
        "cashapp": "Send payment via CashApp to *$myposhsolutions* and reply here with a screenshot.",
        "apple": "Send payment via Apple Pay to *346-475-8302* and reply here with a screenshot.",
        "venmo": "Send payment via Venmo to *@drellanno* and reply here with a screenshot.",
        "crypto": "Choose a crypto:

"
                  "*DOGE*: `D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98`
"
                  "*SOL*: `2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA`
"
                  "*ETH*: `0x96fb9e62981040B7EC09813d15E8a624DBB51311`
"
                  "*USDT (Avalanche)*: `0x96fb9e62981040B7EC09813d15E8a624DBB51311`
"
                  "*XRP (BNB Beacon)*: `bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2`

"
                  "Reply here with the transaction screenshot and crypto used."
    }

    bot.send_message(call.message.chat.id, instructions.get(call.data, "Invalid selection."))
    bot.send_message(call.message.chat.id, f"{ADMIN_USERNAME} — User selected {call.data} for deposit.")

bot.infinity_polling()
Replace bot script with button-based version
