import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_USERNAME = "@GameOnHost"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/app/credentials.json", scope)
client = gspread.authorize(creds)
SHEET_NAME = "Game On Player Ledger"

# Google Sheet logging
def log_transaction_to_sheet(telegram_handle, first_name, sportsbook_username, password, action, amount, method, status):
    try:
        sheet = client.open(SHEET_NAME).sheet1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, telegram_handle, first_name, sportsbook_username, password, action, amount, method, status]
        sheet.append_row(row)
    except Exception as e:
        print("❌ Failed to log to sheet:", e)

# Main menu
def show_inline_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💰 Deposit", callback_data="deposit"),
        InlineKeyboardButton("🏦 Withdraw", callback_data="withdraw"),
        InlineKeyboardButton("🧾 How to Deposit", callback_data="how_to_deposit"),
        InlineKeyboardButton("☎️ Support", callback_data="support")
    )

    welcome_message = (
        "🧿 *Welcome to GameOn*, where the odds work in your favor! 🏆\n\n"
        "🏆 What to expect:\n"
        "• 💵 Easy Deposits (CashApp, Venmo, Apple Pay, Crypto)\n"
        "• 🏦 Fast Withdrawals — every Tuesday after 10AM\n"
        "• 🎁 Exclusive Bonuses & Free Plays\n"
        "• 🧠 Real Humans, Real Help\n\n"
        "Your next win starts here. Choose an option below to begin!"
    )
    bot.send_message(chat_id, welcome_message, reply_markup=markup)

@bot.message_handler(commands=["start"])
def start(message):
    show_inline_main_menu(message.chat.id)

# States
deposit_context = {}
withdraw_context = {}
withdraw_payment_info = {}

# Handle main buttons
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    first_name = call.from_user.first_name
    now = datetime.now()

    if call.data == "deposit":
        deposit_context[chat_id] = True
        bot.send_message(chat_id, f"Hi {first_name}, how much would you like to deposit?", reply_markup=ForceReply())

    elif call.data == "withdraw":
        if now.weekday() == 1 and now.hour >= 10:
            withdraw_context[chat_id] = True
            bot.send_message(chat_id, f"Hi {first_name}, how much would you like to withdraw?", reply_markup=ForceReply())
        else:
            bot.send_message(chat_id,
                "📅 Withdrawals are *only accepted on Tuesdays after 10:00 AM*. Please do not request a payout before then.",
                parse_mode="Markdown"
            )

    elif call.data == "how_to_deposit":
        bot.send_message(chat_id,
            "1. Choose a deposit method\n"
            "2. Send funds to the provided address\n"
            "3. Upload a screenshot here\n"
            "4. We’ll credit your account ASAP ✅",
            parse_mode="Markdown"
        )

    elif call.data == "support":
        bot.send_message(chat_id, "☎️ For help, message @GameOnHost or tag support here and we'll assist you ASAP.")

    elif call.data in ["cashapp", "venmo", "applepay", "crypto"]:
        msg = ""
        if call.data == "cashapp":
            msg = (
                "💸 *Send your deposit to:* `$myposhsolutions`\n\n"
                "📋 If Cash App asks for a note, send just this emoji: 💼\n"
                "⚠️ DO NOT write any words in the note.\n"
                "📷 Upload a screenshot showing the $cashtag after payment.\n\n"
                "*Address expires in 30 minutes.*"
            )
        elif call.data == "venmo":
            msg = (
                "📲 *Send to:* `@drellanno`\n\n"
                "📋 Leave the note blank, or use this emoji: 💼\n"
                "📷 Upload a screenshot once sent to confirm.\n\n"
                "*Address expires in 30 minutes.*"
            )
        elif call.data == "applepay":
            msg = (
                "📱 *Send via Apple Pay to:* `346-475-8302`\n\n"
                "📋 No notes. Screenshot after sending.\n\n"
                "*Address expires in 30 minutes.*"
            )
        elif call.data == "crypto":
            msg = (
                "💱 *Crypto Deposit Addresses:*\n"
                "• Dogecoin: `D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98`\n"
                "• Solana: `2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA`\n"
                "• USDT (AVAX): `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
                "• Ethereum: `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
                "• XRP (BNB Beacon): `bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2`\n\n"
                "📷 Upload a screenshot after sending.\n\n"
                "*Addresses change periodically.*"
            )
        bot.send_message(chat_id, msg, parse_mode="Markdown")

# Deposit amount → method buttons
@bot.message_handler(func=lambda message: deposit_context.get(message.chat.id))
def handle_deposit_amount(message):
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
            InlineKeyboardButton("💱 Crypto", callback_data="crypto")
        )

        bot.send_message(chat_id, f"Thanks {first_name}! Now choose a payment method:", reply_markup=markup)

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

# Handle withdrawal amount
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
        bot.send_message(chat_id, "⚠️ Please enter a valid withdrawal amount (e.g., 100).")

# Payout info
@bot.message_handler(func=lambda msg: withdraw_payment_info.get(msg.chat.id) is not None)
def handle_withdraw_info(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    amount = withdraw_payment_info.pop(chat_id, 0)
    payout = message.text.strip()

    bot.send_message(chat_id,
        f"📝 Thanks {first_name}, we’ve received your request to withdraw *${amount:.2f}* to:\n`{payout}`\n\n"
        "📌 All payouts are processed every *Tuesday after 10AM*.",
        parse_mode="Markdown"
    )

    log_transaction_to_sheet(
        telegram_handle=f"@{message.from_user.username or 'N/A'}",
        first_name=first_name,
        sportsbook_username="N/A",
        password="N/A",
        action="Withdrawal",
        amount=amount,
        method=payout,
        status="Pending"
    )

# Admin: /create_group
@bot.message_handler(commands=["create_group"])
def create_group(message):
    if message.from_user.username != ADMIN_USERNAME.strip("@"):
        return bot.reply_to(message, "❌ You’re not authorized.")

    parts = message.text.strip().split()
    if len(parts) != 2 or not message.reply_to_message:
        return bot.reply_to(message, "⚠️ Usage: /create_group [Username] (must reply to user)")

    user = message.reply_to_message.from_user
    sportsbook_username = parts[1]
    group_title = f"Game On | {sportsbook_username}"

    log_transaction_to_sheet(
        telegram_handle=f"@{user.username or 'N/A'}",
        first_name=user.first_name,
        sportsbook_username=sportsbook_username,
        password="Assigned by VA",
        action="Account Created",
        amount="N/A",
        method="N/A",
        status="Created"
    )

    msg = (
        f"✅ Group setup for *{group_title}*\n\n"
        f"📌 Group Name: *{group_title}*\n"
        f"Add Members: Player, @GameOnSupport, Bot\n\n"
        "📌 Pinned Message:\n"
        "🏆 Welcome to your private Game On betting room!\n"
        "💸 Use the bot to deposit\n"
        "📆 Withdraw on Tuesdays\n"
        "🆘 Contact support anytime\n\n"
        "📍 Let us know when you’re ready to play!"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

# Run bot
bot.infinity_polling()
