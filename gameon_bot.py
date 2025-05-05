import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ForceReply
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_USERNAME = "@GameOnHost"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# Setup Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/app/credentials.json", scope)
client = gspread.authorize(creds)
SHEET_NAME = "Game On Player Ledger"


# Log to sheet
def log_transaction_to_sheet(telegram_handle, first_name, sportsbook_username, password, action, amount, method, status):
    try:
        sheet = client.open(SHEET_NAME).sheet1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, telegram_handle, first_name, sportsbook_username, password, action, amount, method, status]
        sheet.append_row(row)
        print("✅ Logged to Google Sheet.")
    except Exception as e:
        print("❌ Failed to log to sheet:", e)

def show_main_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("💸 Deposit"), KeyboardButton("🏦 Withdraw"))
    markup.add(KeyboardButton("📊 Balance"), KeyboardButton("🧾 How to Deposit"))
    markup.add(KeyboardButton("🆘 Support"))
    welcome_message = (
        "🧿 Welcome to *GameOn*, where the odds work in your favor! 🏆\n\n"
        "🏆 What to expect:\n"
        "• 💵 Easy Deposits (CashApp, Venmo, Apple Pay, Crypto)\n"
        "• 🏦 Fast Withdrawals — every Tuesday\n"
        "• 🎁 Exclusive Bonuses & Free Plays\n"
        "• 🧠 Real Humans, Real Help\n\n"
        "Your next win starts here. Hit \"💸 Deposit\" to get started!"
    )
    bot.send_message(chat_id, welcome_message, reply_markup=markup)

@bot.message_handler(commands=["start"])
def start(message):
    show_main_menu(message.chat.id)
# Deposit flow
deposit_context = {}

@bot.message_handler(func=lambda msg: msg.text == "💸 Deposit")
def start_deposit(message):
    first_name = message.from_user.first_name
    chat_id = message.chat.id
    deposit_context[chat_id] = True
    bot.send_message(chat_id, f"Hi {first_name}, how much would you like to deposit?", reply_markup=ForceReply())

@bot.message_handler(func=lambda message: deposit_context.get(message.chat.id))
def handle_deposit_amount(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name

    try:
        amount = float(message.text.strip().replace("$", ""))
        deposit_context.pop(chat_id, None)

        deposit_msg = (
            f"💵 Great, {first_name}! Here's how to deposit your *${amount:.2f}*:\n\n"
            f"• CashApp: `$myposhsolutions`\n"
            f"• Venmo: `@drellanno`\n"
            f"• Apple Pay: `346-475-8302`\n"
            f"• Crypto Options:\n"
            f"   - Dogecoin: `D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98`\n"
            f"   - Solana: `2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA`\n"
            f"   - USDT (AVAX): `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
            f"   - Ethereum: `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
            f"   - XRP (BNB Beacon): `bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2`\n\n"
            "✅ After you send the payment, reply here with a screenshot so we can credit your account ASAP."
        )
        bot.send_message(chat_id, deposit_msg, parse_mode="Markdown")

        log_transaction_to_sheet(
            telegram_handle=f"@{message.from_user.username or 'N/A'}",
            first_name=first_name,
            sportsbook_username="N/A",
            password="N/A",
            action="Deposit",
            amount=amount,
            method="User Selected",
            status="Pending"
        )

    except ValueError:
        bot.send_message(chat_id, "⚠️ Please enter a valid number for the deposit amount (e.g., 50 or 100).")

# Withdrawal flow
withdraw_context = {}
withdraw_payment_info = {}

@bot.message_handler(func=lambda msg: msg.text == "🏦 Withdraw")
def start_withdraw(message):
    first_name = message.from_user.first_name
    chat_id = message.chat.id
    withdraw_context[chat_id] = True
    bot.send_message(chat_id, f"Hi {first_name}, how much would you like to withdraw?", reply_markup=ForceReply())

@bot.message_handler(func=lambda message: withdraw_context.get(message.chat.id))
def handle_withdraw_amount(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name

    try:
        amount = float(message.text.strip().replace("$", ""))
        withdraw_context.pop(chat_id, None)
        withdraw_payment_info[chat_id] = amount

        bot.send_message(chat_id,
            f"✅ Got it, {first_name}. You've requested to withdraw *${amount:.2f}*.\n\n"
            "Please reply with your payout info (Cash App tag, Venmo username, Apple Pay number, etc.).",
            parse_mode="Markdown"
        )
    except ValueError:
        bot.send_message(chat_id, "⚠️ Please enter a valid number for the withdrawal amount.")

@bot.message_handler(func=lambda message: withdraw_payment_info.get(message.chat.id) is not None)
def handle_withdraw_payout_info(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    amount = withdraw_payment_info.pop(chat_id, 0)
    payout_info = message.text.strip()

    bot.send_message(chat_id,
        f"📝 Thanks {first_name}, we've received your request to withdraw *${amount:.2f}* to:\n`{payout_info}`\n\n"
        "📌 Payouts are processed every *Tuesday*. We’ll notify you once it’s sent.",
        parse_mode="Markdown"
    )

    log_transaction_to_sheet(
        telegram_handle=f"@{message.from_user.username or 'N/A'}",
        first_name=first_name,
        sportsbook_username="N/A",
        password="N/A",
        action="Withdrawal",
        amount=amount,
        method=payout_info,
        status="Pending"
    )
@bot.message_handler(func=lambda msg: msg.text == "🆘 Support")
def support(message):
    bot.send_message(message.chat.id, "For help, message @GameOnHost or tag support here and we'll assist you ASAP.")

@bot.message_handler(func=lambda msg: msg.text == "📊 Balance")
def balance(message):
    bot.send_message(message.chat.id, "To check your balance, message @GameOnHost or wait for it to be updated here.")

@bot.message_handler(func=lambda msg: msg.text == "🧾 How to Deposit")
def how_to_deposit(message):
    bot.send_message(message.chat.id,
        "1. Choose a deposit method\n"
        "2. Send funds to the provided address\n"
        "3. Upload a screenshot here\n"
        "4. We’ll credit your account ASAP ✅",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['create_group'])
def create_group(message):
    if message.from_user.username != ADMIN_USERNAME.strip('@'):
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    try:
        parts = message.text.strip().split()
        if len(parts) != 2:
            bot.reply_to(message, "⚠️ Usage: /create_group [SportsbookUsername]")
            return

        sportsbook_username = parts[1]

        if not message.reply_to_message:
            bot.reply_to(message, "⚠️ Please reply to the user's message when using this command.")
            return

        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        telegram_handle = f"@{message.reply_to_message.from_user.username or 'N/A'}"
        group_title = f"Game On | {sportsbook_username}"

        # Optional: Log group creation with credentials
        log_transaction_to_sheet(
            telegram_handle=telegram_handle,
            first_name=first_name,
            sportsbook_username=sportsbook_username,
            password="Assigned by VA",
            action="Account Created",
            amount="N/A",
            method="N/A",
            status="Created"
        )

        template = (
            f"📌 Group Setup Template:\n"
            f"Group Name: *{group_title}*\n"
            f"Add Members: Player, @GameOnSupport, Bot\n\n"
            f"Pinned Message:\n"
            "🏆 Welcome to your private Game On betting room!\n\n"
            "This group is just for you — no distractions, no spam.\n"
            "💸 Deposit with the bot\n"
            "📊 Check your balance\n"
            "🆘 Get help when needed\n\n"
            "📌 Let us know when you're ready to deposit!"
        )

        bot.reply_to(message, f"✅ Group setup for: *{group_title}*\n\n{template}", parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Failed to setup group: {str(e)}")
# Start the bot
bot.infinity_polling()






