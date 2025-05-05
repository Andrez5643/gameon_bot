import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
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

# Main menu with inline buttons
def show_inline_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💰 Deposit", callback_data="deposit"),
        InlineKeyboardButton("🏦 Withdraw", callback_data="withdraw"),
        InlineKeyboardButton("📊 Balance", callback_data="balance"),
        InlineKeyboardButton("🧾 How to Deposit", callback_data="how_to_deposit"),
        InlineKeyboardButton("☎️ Support", callback_data="support")
    )

    welcome_message = (
        "🧿 *Welcome to GameOn*, where the odds work in your favor! 🏆\n\n"
        "🏆 What to expect:\n"
        "• 💵 Easy Deposits (CashApp, Venmo, Apple Pay, Crypto)\n"
        "• 🏦 Fast Withdrawals — every Tuesday\n"
        "• 🎁 Exclusive Bonuses & Free Plays\n"
        "• 🧠 Real Humans, Real Help\n\n"
        "Your next win starts here. Choose an option below to begin!"
    )

    bot.send_message(chat_id, welcome_message, reply_markup=markup)

@bot.message_handler(commands=["start"])
def start(message):
    show_inline_main_menu(message.chat.id)

# State tracking
deposit_context = {}
withdraw_context = {}
withdraw_payment_info = {}

# Inline button callback handler
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    first_name = call.from_user.first_name

    if call.data == "deposit":
        deposit_context[chat_id] = True
        bot.send_message(chat_id, f"Hi {first_name}, how much would you like to deposit?", reply_markup=ForceReply())

    elif call.data == "withdraw":
        withdraw_context[chat_id] = True
        bot.send_message(chat_id, f"Hi {first_name}, how much would you like to withdraw?", reply_markup=ForceReply())

    elif call.data == "balance":
        bot.send_message(chat_id, "📊 To check your balance, message @GameOnHost or wait for it to be updated here.")

    elif call.data == "how_to_deposit":
        bot.send_message(chat_id,
            """1. Choose a deposit method  
2. Send funds to the provided address  
3. Upload a screenshot here  
4. We’ll credit your account ASAP ✅""",
            parse_mode="Markdown"
        )

    elif call.data == "support":
        bot.send_message(chat_id, "☎️ For help, message @GameOnHost or tag support here and we'll assist you ASAP.")

# Deposit amount handler
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

# Withdraw amount handler
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

bot.infinity_polling()
