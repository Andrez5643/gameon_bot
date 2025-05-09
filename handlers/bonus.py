from telebot.types import ForceReply, CallbackQuery
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

        # Start 10-minute reminder timer
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

    @bot.message_handler(func=lambda message: message.chat.id in deposit_context)
    def handle_deposit_amount(message):
        chat_id = message.chat.id
        first_name = message.from_user.first_name
        username = message.from_user.username or "N/A"

        try:
            amount = float(message.text.strip().replace("$", ""))
        except ValueError:
            bot.send_message(chat_id, "⚠️ Please enter a valid number (e.g., 100).")
            return

        # Clean up
        deposit_context.pop(chat_id, None)
        if chat_id in reminder_timers:
            reminder_timers[chat_id].cancel()
            reminder_timers.pop(chat_id)

        if amount < 50:
            bot.send_message(chat_id,
                "⚠️ The *minimum deposit is $100* to continue.\n"
                "We can occasionally accept as low as *$50*, but unfortunately, *${amount:.2f}* won’t qualify. Please try again.",
                parse_mode="Markdown"
            )
            return

        # ✅ Approved deposit
        bot.send_message(chat_id,
            f"💵 Great, {first_name}! Here's how to deposit your *${amount:.2f}*:\n\n"
            f"• CashApp: `$myposhsolutions`\n"
            f"• Venmo: `@drellanno`\n"
            f"• Apple Pay: `346-475-8302`\n"
            f"• Crypto:\n"
            f"  - Dogecoin: `D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98`\n"
            f"  - Solana: `2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA`\n"
            f"  - USDT (AVAX): `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
            f"  - Ethereum: `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
            f"  - XRP (BNB Beacon): `bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2`\n\n"
            "✅ After sending, reply here with a screenshot so we can credit your account ASAP.",
            parse_mode="Markdown"
        )

        # Start 30-minute expiration reminders
        start_expiration_timer(bot, chat_id, method="Deposit")

        # Log to Sheets
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

