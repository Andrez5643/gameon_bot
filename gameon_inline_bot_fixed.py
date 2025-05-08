import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_USERNAME = "@GameOnHost"
SHEET_NAME = "Game On Player Ledger"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/app/credentials.json", scope)
client = gspread.authorize(creds)

def log_transaction_to_sheet(telegram_handle, first_name, sportsbook_username, password, action, amount, method, status):
    try:
        sheet = client.open(SHEET_NAME).sheet1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, telegram_handle, first_name, sportsbook_username, password, action, amount, method, status]
        sheet.append_row(row)
        print("✅ Logged to Google Sheet.")
    except Exception as e:
        print("❌ Failed to log to sheet:", e)

def show_inline_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💰 Deposit", callback_data="deposit"),
        InlineKeyboardButton("🏦 Withdraw", callback_data="withdraw"),
        InlineKeyboardButton("🧾 How to Deposit", callback_data="how_to_deposit"),
        InlineKeyboardButton("☎️ Support", callback_data="support")
    )
    welcome = (
        "🧿 *Welcome to GameOn*, where the odds work in your favor! 🏆\n\n"
        "🏆 What to expect:\n"
        "• 💵 Easy Deposits (CashApp, Venmo, Apple Pay, Crypto)\n"
        "• 🏦 Fast Withdrawals — every Tuesday after 10AM\n"
        "• 🎁 Exclusive Bonuses & Free Plays\n"
        "• 🧠 Real Humans, Real Help\n\n"
        "Your next win starts here. Choose an option below to begin!"
    )
    bot.send_message(chat_id, welcome, reply_markup=markup)

# ========== START + AFFILIATE ==========
affiliate_referrals = {}

@bot.message_handler(commands=["start"])
def handle_start(message):
    chat_id = message.chat.id
    text = message.text.strip()
    first_name = message.from_user.first_name
    username = message.from_user.username or "N/A"

    parts = text.split()
    if len(parts) == 2 and parts[1].startswith("af_"):
        affiliate_id = parts[1][3:]
        affiliate_referrals[chat_id] = affiliate_id
        bot.send_message(chat_id,
            f"👋 Welcome {first_name}!\n\nYou were referred by: *{affiliate_id}*\n\n"
            "Let's get you started with Game On Sportsbook.",
            parse_mode="Markdown"
        )
        log_transaction_to_sheet(f"@{username}", first_name, "N/A", "N/A", "Referral", "N/A", f"Affiliate: {affiliate_id}", "New Lead")
    else:
        show_inline_main_menu(chat_id)

# ========== DEPOSIT FLOW ==========
deposit_context = {}

@bot.callback_query_handler(func=lambda call: call.data == "deposit")
def ask_deposit_amount(call):
    chat_id = call.message.chat.id
    deposit_context[chat_id] = True
    bot.send_message(chat_id, "How much would you like to deposit?", reply_markup=ForceReply())

@bot.message_handler(func=lambda msg: deposit_context.get(msg.chat.id))
def ask_payment_method(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    try:
        amount = float(message.text.strip().replace("$", ""))
        deposit_context.pop(chat_id, None)
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("💸 Cash App", callback_data="cashapp"),
            InlineKeyboardButton("📲 Venmo", callback_data="venmo"),
            InlineKeyboardButton("📱 Apple Pay", callback_data="applepay"),
            InlineKeyboardButton("🪙 Crypto", callback_data="crypto")
        )
        bot.send_message(chat_id, f"Thanks {first_name}! Choose a payment method below:", reply_markup=markup)
    except ValueError:
        bot.send_message(chat_id, "⚠️ Please enter a valid number (e.g., 50 or 100).")

@bot.callback_query_handler(func=lambda call: call.data in ["cashapp", "venmo", "applepay", "crypto"])
def show_payment_details(call):
    msg = ""
    if call.data == "cashapp":
        msg = "💸 Send to: `$myposhsolutions`\n✅ Leave the note blank. Send a screenshot after."
    elif call.data == "venmo":
        msg = "📲 Send to: `@drellanno`\n✅ Blank note or ✅ only. Screenshot required."
    elif call.data == "applepay":
        msg = "📱 Send via Apple Pay: `346-475-8302`\n✅ No notes. Screenshot after sending."
    elif call.data == "crypto":
        msg = (
            "🪙 *Crypto Options:*\n"
            "- Dogecoin: `D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98`\n"
            "- Solana: `2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA`\n"
            "- USDT (AVAX): `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
            "- Ethereum: `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
            "- XRP (BNB Beacon): `bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2`\n\n"
            "✅ Reply with a screenshot after payment."
        )
    bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")

# ========== WITHDRAWAL ==========
withdraw_context = {}
withdraw_payment_info = {}

@bot.callback_query_handler(func=lambda call: call.data == "withdraw")
def handle_withdraw_start(call):
    chat_id = call.message.chat.id
    first_name = call.from_user.first_name
    now = datetime.now()
    if now.weekday() == 1 and now.hour >= 10:
        withdraw_context[chat_id] = True
        bot.send_message(chat_id, f"Hi {first_name}, how much would you like to withdraw?", reply_markup=ForceReply())
    else:
        bot.send_message(chat_id,
            "📅 Withdrawals are *only accepted on Tuesdays after 10:00 AM*. Please come back then.",
            parse_mode="Markdown"
        )

@bot.message_handler(func=lambda msg: withdraw_context.get(msg.chat.id))
def handle_withdraw_amount(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    try:
        amount = float(message.text.strip().replace("$", ""))
        withdraw_context.pop(chat_id, None)
        withdraw_payment_info[chat_id] = amount
        bot.send_message(chat_id,
            f"✅ Got it, {first_name}. You've requested *${amount:.2f}*.\nReply with your payout info (Cash App, Venmo, etc.):",
            parse_mode="Markdown"
        )
    except ValueError:
        bot.send_message(chat_id, "⚠️ Invalid amount. Please try again.")

@bot.message_handler(func=lambda msg: withdraw_payment_info.get(msg.chat.id) is not None)
def handle_withdraw_payout_info(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    amount = withdraw_payment_info.pop(chat_id, 0)
    payout_info = message.text.strip()
    bot.send_message(chat_id,
        f"📝 Request to withdraw *${amount:.2f}* to:\n`{payout_info}`\n\n📌 Payouts sent every *Tuesday*.",
        parse_mode="Markdown"
    )
    log_transaction_to_sheet(f"@{message.from_user.username or 'N/A'}", first_name, "N/A", "N/A", "Withdrawal", amount, payout_info, "Pending")

# ========== SUPPORT & HELP ==========
@bot.callback_query_handler(func=lambda call: call.data == "how_to_deposit")
def how_to_deposit(call):
    bot.send_message(call.message.chat.id,
        "1. Choose a deposit method\n2. Send payment\n3. Upload screenshot here\n4. We’ll credit ASAP ✅",
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "support")
def support(call):
    bot.send_message(call.message.chat.id, "☎️ For help, message @GameOnHost or tag support here.")

# ========== ADMIN GROUP CREATION ==========
@bot.message_handler(commands=["create_group"])
def create_group(message):
    if message.from_user.username != ADMIN_USERNAME.strip("@"):
        bot.reply_to(message, "❌ You are not authorized.")
        return
    try:
        parts = message.text.strip().split()
        if len(parts) != 2 or not message.reply_to_message:
            bot.reply_to(message, "⚠️ Usage: /create_group [SportsbookUsername] (as a reply to the player)")
            return

        sportsbook_username = parts[1]
        user = message.reply_to_message.from_user
        telegram_handle = f"@{user.username or 'N/A'}"
        first_name = user.first_name
        group_title = f"Game On | {sportsbook_username}"

        log_transaction_to_sheet(telegram_handle, first_name, sportsbook_username, "Assigned by VA", "Account Created", "N/A", "N/A", "Created")

        template = (
            f"✅ Group setup for: *{group_title}*\n\n"
            f"📌 Group Name: *{group_title}*\n"
            "Add: Player, @GameOnSupport, Bot\n\n"
            "🏆 Welcome to your private Game On room!\n"
            "💸 Deposit with the bot\n"
            "🧾 How to Deposit anytime\n"
            "🆘 Get help\n\n"
            "📌 Let us know when you're ready to deposit!"
        )
        bot.reply_to(message, template, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Group setup failed: {e}")

# ========== START POLLING ==========
bot.infinity_polling()
