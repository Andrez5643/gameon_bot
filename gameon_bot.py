import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USERNAME = "@KaliDapper"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("💸 Deposit"),
        KeyboardButton("💵 Withdraw")
    )
    markup.add(
        KeyboardButton("📊 Balance"),
        KeyboardButton("📥 How to Deposit"),
        KeyboardButton("🧑‍💻 Support")
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
    bot.send_message(message.chat.id, "💸 Send payment via *CashApp* to `$myposhsolutions` and reply with a screenshot.")
    bot.send_message(ADMIN_USERNAME, f"{message.from_user.first_name} selected CashApp to deposit.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() == "apple pay")
def applepay(message):
    bot.send_message(message.chat.id, "📱 Send payment via *Apple Pay* to `346-475-8302` and reply with a screenshot.")
    bot.send_message(ADMIN_USERNAME, f"{message.from_user.first_name} selected Apple Pay to deposit.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() == "venmo")
def venmo(message):
    bot.send_message(message.chat.id, "🏦 Send payment via *Venmo* to `@drellanno` and reply with a screenshot.")
    bot.send_message(ADMIN_USERNAME, f"{message.from_user.first_name} selected Venmo to deposit.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() == "crypto")
def crypto(message):
    bot.send_message(message.chat.id, """💰 *Choose a crypto method:*

*DOGE*: `D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98`
*SOL*: `2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA`
*ETH*: `0x96fb9e62981040B7EC09813d15E8a624DBB51311`
*USDT (Avalanche)*: `0x96fb9e62981040B7EC09813d15E8a624DBB51311`
*XRP (BNB Beacon)*: `bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2`

Reply with the transaction screenshot and crypto used.""")
    bot.send_message(ADMIN_USERNAME, f"{message.from_user.first_name} selected Crypto to deposit.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() in ["💵 withdraw", "withdraw", "cashout"])
def withdraw(message):
    bot.send_message(message.chat.id, f"💵 Withdrawals are handled manually. Contact our agent: {ADMIN_USERNAME}")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() in ["📊 balance", "balance"])
def balance(message):
    bot.send_message(message.chat.id, f"📊 To check your balance, message: {ADMIN_USERNAME}")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() in ["📥 how to deposit", "how to deposit"])
def howtodeposit(message):
    bot.send_message(message.chat.id, "📥 To deposit, select 'Deposit' from the menu and follow the steps.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.lower() in ["🧑‍💻 support", "support"])
def support(message):
    bot.send_message(message.chat.id, f"🧑‍💻 For support, please message: {ADMIN_USERNAME}")

bot.infinity_polling()



