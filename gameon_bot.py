import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='Markdown')

admin_username = "@KaliDapper"  # Admin gets alerts here

# 🏁 /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Deposit", "📞 Support")
    bot.send_message(message.chat.id, "👋 *Welcome to GameOn Assistance!*\n\nChoose an option below:", reply_markup=markup)

# 🔁 Handle text-based main menu selections
@bot.message_handler(func=lambda message: message.text == "💰 Deposit")
def deposit_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💸 Cash App", callback_data="cashapp"),
        types.InlineKeyboardButton("🅿️ Venmo", callback_data="venmo")
    )
    markup.add(
        types.InlineKeyboardButton("🍎 Apple Pay", callback_data="applepay"),
        types.InlineKeyboardButton("🪙 Crypto", callback_data="crypto")
    )
    bot.send_message(message.chat.id, "*Select a deposit method:*", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📞 Support")
def support(message):
    bot.send_message(message.chat.id, f"📞 For help, message {admin_username}")

# 🔘 Handle deposit method selection
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "cashapp":
        ask_amount(call.message, "Cash App", "$myposhsolutions")
    elif call.data == "venmo":
        ask_amount(call.message, "Venmo", "@drellanno")
    elif call.data == "applepay":
        ask_amount(call.message, "Apple Pay", "346-475-8302")
    elif call.data == "crypto":
        crypto_menu(call.message)
    elif call.data.startswith("crypto_"):
        crypto_type = call.data.split("_")[1]
        crypto_address = {
            "btc": "BTC: [Wallet Needed]",
            "eth": "0x96fb9e62981040B7EC09813d15E8a624DBB51311",
            "usdt": "0x96fb9e62981040B7EC09813d15E8a624DBB51311",
            "sol": "2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA",
            "xrp": "bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2",
            "doge": "D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98"
        }
        ask_amount(call.message, crypto_type.upper(), crypto_address[crypto_type])

def crypto_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💰 Bitcoin", callback_data="crypto_btc"),
        types.InlineKeyboardButton("💰 Ethereum", callback_data="crypto_eth"),
        types.InlineKeyboardButton("💰 USDT (Avalanche)", callback_data="crypto_usdt")
    )
    markup.add(
        types.InlineKeyboardButton("💰 Solana", callback_data="crypto_sol"),
        types.InlineKeyboardButton("💰 XRP", callback_data="crypto_xrp"),
        types.InlineKeyboardButton("💰 Dogecoin", callback_data="crypto_doge")
    )
    bot.send_message(message.chat.id, "*Select a crypto method:*", reply_markup=markup)

# 🧾 Ask user to confirm amount after method selected
def ask_amount(message, method, payment_info):
    bot.send_message(message.chat.id, f"*Send your deposit via {method}:*\n\n➡️ `{payment_info}`\n\nPlease reply with the amount you sent:")
    bot.register_next_step_handler(message, lambda m: confirm_deposit(m, method, payment_info))

# ✅ Confirm deposit & notify admin
def confirm_deposit(message, method, payment_info):
    amount = message.text.strip()
    bot.send_message(message.chat.id, f"✅ Got it! You reported a *{amount}* deposit via *{method}*.\n\nWe'll confirm and credit you shortly.")
    bot.send_message(message.chat.id, "📸 Don’t forget to send a screenshot of your payment!")

    # Admin alert
    bot.send_message(message.chat.id, "📨 Your request has been forwarded to support.")
    bot.send_message(admin_username,
        f"💰 *New Deposit Alert!*\n\n"
        f"👤 From: @{message.from_user.username}\n"
        f"💳 Method: {method}\n"
        f"💵 Amount: {amount}\n"
        f"📍 Sent to: `{payment_info}`"
    )

# 🚀 Start bot
print("✅ GameOn Assistance Bot running...")
bot.infinity_polling()

