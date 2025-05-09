import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.deposit import register_deposit_handlers
from handlers.withdraw import register_withdraw_handlers
from handlers.support import register_support_handler
from handlers.bonus import handle_bonus_claim

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# 📍 Main menu layout
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💰 Deposit", callback_data="deposit"),
        InlineKeyboardButton("🏦 Withdraw", callback_data="withdraw"),
        InlineKeyboardButton("🧾 How to Deposit", callback_data="how_to_deposit"),
        InlineKeyboardButton("☎️ Support", callback_data="support"),
        InlineKeyboardButton("🎁 Claim Bonus", callback_data="claim_bonus")
    )

    welcome_text = (
        "🧿 *Welcome to GameOn*, where the odds work in your favor! 🏆\n\n"
        "🏆 What to expect:\n"
        "• 💵 Easy Deposits (CashApp, Venmo, Apple Pay, Crypto)\n"
        "• 🏦 Fast Withdrawals — every Tuesday after 10AM\n"
        "• 🎁 Exclusive Bonuses & Free Plays\n"
        "• 🧠 Real Humans, Real Help\n\n"
        "Your next win starts here. Choose an option below to begin!"
    )

    bot.send_message(chat_id, welcome_text, reply_markup=markup)

# 📌 Register all handlers
register_deposit_handlers(bot)
register_withdraw_handlers(bot)
register_support_handler(bot)

# 🎁 Register bonus claim handler
bot.register_callback_query_handler(handle_bonus_claim, lambda call: call.data == "claim_bonus")

# ▶️ /start command
@bot.message_handler(commands=["start"])
def start(message):
    show_main_menu(message.chat.id)

# 🟢 Launch the bot
if __name__ == "__main__":
    print("🚀 GameOn Bot is live and polling...")
    bot.infinity_polling()
