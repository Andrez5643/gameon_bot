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

    welcome_message = (
        "🧿 Welcome to *GameOn*, where the odds work in your favor! 🏆\n\n"
        "We're more than just a sportsbook — we're your personal line to big wins, fast payouts, and premium support. ✅\n\n"
        "🏆 What to expect:\n"
        "• 💵 Easy Deposits (CashApp, Venmo, Apple Pay, Crypto)\n"
        "• 🏦 Fast Withdrawals — every Tuesday\n"
        "• 🎁 Exclusive Bonuses & Free Plays\n"
        "• 🧠 Real Humans, Real Help\n\n"
        "Your next win starts here. If you ever need support, tap 🆘 or message @GameOnHost.\n\n"
        "💬 Hit \"💸 Deposit\" to get started!"
    )

    bot.send_message(chat_id, welcome_message, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=["start"])
def start(message):
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda msg: msg.text == "_
@bot.message_handler(func=lambda msg: msg.text in ["CashApp", "Apple Pay", "Venmo", "Crypto"])
def handle_deposit_method(message):
    methods = {
        "CashApp": "$myposhsolutions",
        "Apple Pay": "346-475-8302",
        "Venmo": "@drellanno",
        "Crypto": (
            "🪙 *Crypto Deposit Addresses:*\n"
            "• Dogecoin: `D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98`\n"
            "• Solana: `2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA`\n"
            "• USDT (AVAX): `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
            "• Ethereum: `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
            "• XRP (BNB Beacon): `bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2`"
        )
    }

    if message.text == "Crypto":
        bot.send_message(message.chat.id, methods["Crypto"], parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, f"Send your deposit to:\n*{methods[message.text]}*", parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "⬅️ Back")
def go_back(message):
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda msg: msg.text == "🆘 Support")
def support(message):
    bot.send_message(message.chat.id, "For help, message @GameOnHost or tag support here and we'll assist you ASAP.")

@bot.message_handler(func=lambda msg: msg.text == "📊 Balance")
def balance(message):
    bot.send_message(message.chat.id, "To check your balance, please message @GameOnHost or wait for it to be updated here.")

@bot.message_handler(func=lambda msg: msg.text == "🧾 How to Deposit")
def how_to_deposit(message):
    bot.send_message(message.chat.id,
        "1. Choose a deposit method.\n"
        "2. Send funds to the provided handle/address.\n"
        "3. Upload a screenshot for confirmation.\n"
        "4. We'll credit your account ASAP. ✅",
        parse_mode="Markdown"
    )

# ✅ /create_group command with sportsbook username
@bot.message_handler(commands=['create_group'])
def create_group(message):
    if message.from_user.username != ADMIN_USERNAME.strip('@'):
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    try:
        command_parts = message.text.strip().split()
        if len(command_parts) != 2:
            bot.reply_to(message, "⚠️ Usage: /create_group [SportsbookUsername]")
            return

        sportsbook_username = command_parts[1]

        if not message.reply_to_message:
            bot.reply_to(message, "⚠️ Please reply to the user's message when using this command.")
            return

        user_id = message.reply_to_message.from_user.id
        group_title = f"Game On | {sportsbook_username}"

        # --- Setup Template for VA ---
        va_template = (
            f"📌 Group Setup Template:\n"
            f"Group Name: *{group_title}*\n"
            f"Add Members: Player, @GameOnSupport, Bot\n\n"
            f"Pinned Message:\n"
            "🏆 Welcome to your private Game On betting room!\n\n"
            "This group is just for you — no distractions, no spam.\n\n"
            "Here’s what you can do:\n"
            "💸 Deposit using the bot\n"
            "📊 Check your balance\n"
            "🆘 Request withdrawals or support\n\n"
            "📌 All activity is handled right here.\n"
            "Let us know when you're ready to deposit!"
        )

        bot.reply_to(message, f"✅ Group setup would proceed for: *{group_title}*\n\n{va_template}", parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Failed to setup group: {str(e)}")

# 🚀 Start polling
bot.infinity_polling()





