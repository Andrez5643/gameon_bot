from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply
from utils.sheets import log_transaction_to_sheet
from utils.timers import start_expiration_timer
from datetime import datetime
from threading import Timer

deposit_context = {}
reminder_timers = {}

def register_deposit_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "deposit")
    def ask_deposit_amount(call: CallbackQuery):
        chat_id = call.message.chat.id
        first_name = call.from_user.first_name
        deposit_context[chat_id] = {"start_time": datetime.now()}

        bot.send_message(chat_id, f"Hi {first_name}, how much would you like to deposit?", reply_markup=ForceReply())

        def remind_user():
            if chat_id in deposit_context:
                bot.send_message(chat_id,
                    "⏳ Just a reminder — the *minimum deposit is $100* to continue.\n\n"
                    "✅ That said, we will quietly accept *$50 or more* *this time for your convenience.*\n"
                    "Just be aware that moving forward, the *minimum deposit is $100.*",
                    parse_mode="Markdown"
                )

        reminder_timers[chat_id] = Timer(600, remind_user)
        reminder_timers[chat_id].start()

    @bot.message_handler(func=lambda msg: msg.chat.id in deposit_context)
    def handle_deposit_amount(message):
        chat_id = message.chat.id
        first_name = message.from_user.first_name
        username = message.from_user.username or "N/A"

        try:
            amount = float(message.text.strip().replace("$", ""))
        except ValueError:
            bot.send_message(chat_id, "⚠️ Please enter a valid number (e.g., 100).")
            return

        if amount < 50:
            bot.send_message(chat_id,
                f"⚠️ The *minimum deposit is $100* to continue.\n"
                f"We can occasionally accept as low as *$50*, but *${amount:.2f}* won’t qualify.",
                parse_mode="Markdown"
            )
            return

        deposit_context.pop(chat_id, None)
        if chat_id in reminder_timers:
            reminder_timers[chat_id].cancel()
            reminder_timers.pop(chat_id)

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("💵 Cash App", callback_data="cashapp"),
            InlineKeyboardButton("📲 Venmo", callback_data="venmo"),
            InlineKeyboardButton("📱 Apple Pay", callback_data="applepay"),
            InlineKeyboardButton("🪙 Crypto", callback_data="crypto")
        )
        bot.send_message(chat_id, f"Thanks {first_name}! Choose a payment method below:", reply_markup=markup)

        log_transaction_to_sheet(
            telegram_handle=f"@{username}",
            first_name=first_name,
            sportsbook_username="N/A",
            password="N/A",
            action="Deposit",
            amount=amount,
            method="User Selected",
            status="Pending"
        )

    @bot.callback_query_handler(func=lambda call: call.data in ["cashapp", "venmo", "applepay", "crypto"])
    def show_payment_info(call):
        method = call.data
        chat_id = call.message.chat.id

        if method == "cashapp":
            msg = "💵 Send your deposit to: `$myposhsolutions`\n\n✅ Leave the note blank and send a screenshot here."
        elif method == "venmo":
            msg = "📲 Send your deposit to: `@drellanno`\n\n✅ Leave the note blank or use ✅. Screenshot required."
        elif method == "applepay":
            msg = "📱 Apple Pay #: `346-475-8302`\n\n✅ No notes. Just send, then upload a screenshot here."
        elif method == "crypto":
            msg = (
                "🪙 *Crypto Wallets:*\n"
                "- Dogecoin: `D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98`\n"
                "- Solana: `2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA`\n"
                "- USDT (AVAX): `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
                "- Ethereum: `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
                "- XRP (BNB Beacon): `bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2`\n\n"
                "✅ After sending, reply with a screenshot to confirm."
            )

        bot.send_message(chat_id, msg, parse_mode="Markdown")

        # Start expiration timer after showing payment info
        start_expiration_timer(bot, chat_id, method=method.capitalize())

def register_how_to_deposit_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "how_to_deposit")
    def handle_how_to_deposit(call):
        bot.send_message(call.message.chat.id,
            "🧾 *How to Deposit*\n\n"
            "1. Tap *Deposit* and enter how much you want to send\n"
            "2. Choose your payment method\n"
            "3. Send funds to the address provided\n"
            "4. Upload a screenshot here\n\n"
            "💸 We’ll credit your account ASAP!",
            parse_mode="Markdown"
        )

