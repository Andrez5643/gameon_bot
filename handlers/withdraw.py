from telebot.types import ForceReply
from datetime import datetime
from utils.sheets import log_transaction_to_sheet

withdraw_context = {}
withdraw_payment_info = {}

def register_withdraw_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "withdraw")
    def ask_withdraw(call):
        chat_id = call.message.chat.id
        first_name = call.from_user.first_name
        now = datetime.now()

        # Allow requests only on Tuesday — if it's before 10AM, accept; if after, delay
        if now.weekday() == 1:  # Tuesday
            if now.hour < 10:
                bot.send_message(chat_id,
                    "📅 Withdrawals are processed every *Tuesday after 10:00 AM*.\n"
                    "⚠️ You've requested too early — please check back after 10:00 AM.",
                    parse_mode="Markdown"
                )
            elif now.hour >= 10 and now.hour <= 23:
                # If Tuesday but after 10AM — deny for this week (too late)
                bot.send_message(chat_id,
                    "⚠️ Withdrawal requests must be made *before Tuesday* to be processed this week.\n"
                    "✅ Your request will be included in *next Tuesday's* payout cycle.",
                    parse_mode="Markdown"
                )
                withdraw_context[chat_id] = "next_week"
                bot.send_message(chat_id, f"Hi {first_name}, how much would you like to withdraw?", reply_markup=ForceReply())
        else:
            # Not Tuesday — schedule for upcoming Tuesday
            withdraw_context[chat_id] = "next_week"
            bot.send_message(chat_id, f"Hi {first_name}, how much would you like to withdraw?", reply_markup=ForceReply())

    @bot.message_handler(func=lambda message: withdraw_context.get(message.chat.id))
    def get_withdraw_amount(message):
        chat_id = message.chat.id
        first_name = message.from_user.first_name

        try:
            amount = float(message.text.strip().replace("$", ""))
            withdraw_payment_info[chat_id] = amount
            withdraw_context.pop(chat_id, None)

            bot.send_message(chat_id,
                f"✅ Got it, {first_name}. You've requested to withdraw *${amount:.2f}*.\n\n"
                "Please reply with your payout info (Cash App tag, Venmo username, Apple Pay number, etc.):",
                parse_mode="Markdown"
            )
        except ValueError:
            bot.send_message(chat_id, "⚠️ Please enter a valid amount (e.g., 50 or 100).")

    @bot.message_handler(func=lambda message: withdraw_payment_info.get(message.chat.id) is not None)
    def get_payout_details(message):
        chat_id = message.chat.id
        user = message.from_user
        username = user.username or "N/A"
        first_name = user.first_name
        payout_info = message.text.strip()
        amount = withdraw_payment_info.pop(chat_id)

        bot.send_message(chat_id,
            f"📝 Thanks {first_name}, we've received your request to withdraw *${amount:.2f}* to:\n"
            f"`{payout_info}`\n\n"
            "📌 It will be processed *next Tuesday* by our payout team. ✅",
            parse_mode="Markdown"
        )

        log_transaction_to_sheet(
            telegram_handle=f"@{username}",
            first_name=first_name,
            sportsbook_username="N/A",
            password="N/A",
            action="Withdrawal",
            amount=amount,
            method=payout_info,
            status="Pending"
        )
