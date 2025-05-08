from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from utils.sheets import log_transaction_to_sheet
from utils.timers import start_expiration_timer

deposit_context = {}

def register_deposit_handlers(bot):
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
                InlineKeyboardButton("💸 Cash App", callback_data=f"pay_cashapp_{amount}"),
                InlineKeyboardButton("📲 Venmo", callback_data=f"pay_venmo_{amount}"),
                InlineKeyboardButton("📱 Apple Pay", callback_data=f"pay_apple_{amount}"),
                InlineKeyboardButton("🪙 Crypto", callback_data=f"pay_crypto_{amount}")
            )

            bot.send_message(chat_id, f"Thanks {first_name}! Choose a payment method:", reply_markup=markup)

        except ValueError:
            bot.send_message(chat_id, "⚠️ Please enter a valid amount (e.g., 50 or 100).")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
    def send_payment_instructions(call):
        chat_id = call.message.chat.id
        username = call.from_user.username or "N/A"
        first_name = call.from_user.first_name

        _, method, amount_str = call.data.split("_")
        amount = float(amount_str)

        messages = {
            "cashapp": (
                "💸 *CashApp:* `$myposhsolutions`\n\n"
                "📌 *Note:* Leave the note blank. If Cash App requires a note, use this emoji: 💼\n"
                "🕒 Address will expire in 30 minutes. We'll remind you at 10, 5, and 1 minute before expiration.\n\n"
                "✅ After sending, reply with a screenshot."
            ),
            "venmo": (
                "📲 *Venmo:* `@drellanno`\n\n"
                "📌 *Note:* Leave blank or use ✅ if required.\n"
                "🕒 Address expires in 30 minutes with reminders.\n\n"
                "✅ Reply with a screenshot after payment."
            ),
            "apple": (
                "📱 *Apple Pay:* `346-475-8302`\n\n"
                "🕒 This number will expire in 30 minutes.\n\n"
                "✅ Send your payment and reply here with a screenshot."
            ),
            "crypto": (
                "🪙 *Crypto Wallets:*\n"
                "- Dogecoin: `D8FiDJhqr2LcxHtqroywc1Y5yrF6tMom98`\n"
                "- Solana: `2FnSCWLh5fVB4Fpjbi7TuaTPu9HtNZexiTu5SbDm6XTA`\n"
                "- USDT (AVAX): `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
                "- Ethereum: `0x96fb9e62981040B7EC09813d15E8a624DBB51311`\n"
                "- XRP (BNB): `bnb12awmj04d0csswhf5cyt66fzmwl4chfrrvhvhx2`\n\n"
                "🕒 Wallets expire in 30 minutes. We'll notify you before expiration.\n\n"
                "✅ Send and upload screenshot here."
            )
        }

        text = messages.get(method, "⚠️ Invalid method. Please try again.")
        bot.send_message(chat_id, text, parse_mode="Markdown")

        log_transaction_to_sheet(
            telegram_handle=f"@{username}",
            first_name=first_name,
            sportsbook_username="N/A",
            password="N/A",
            action="Deposit",
            amount=amount,
            method=method.capitalize(),
            status="Pending"
        )

        start_expiration_timer(bot, chat_id, method, minutes=30)
