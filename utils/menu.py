from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def show_main_menu(bot, chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💰 Deposit", callback_data="deposit"),
        InlineKeyboardButton("🏦 Withdraw", callback_data="withdraw"),
        InlineKeyboardButton("🧾 How to Deposit", callback_data="how_to_deposit"),
        InlineKeyboardButton("🏛️ Support", callback_data="support"),
    )
    bot.send_message(chat_id, "📲 *Main Menu* — Please choose an option below:", reply_markup=markup, parse_mode="Markdown")
