import os
import telebot
from handlers.deposit import register_deposit_handlers
from handlers.withdraw import register_withdraw_handlers
from handlers.bonus import register_bonus_handlers
from handlers.support import register_support_handler
from utils.menu import show_main_menu

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# Register all feature handlers
register_deposit_handlers(bot)
register_withdraw_handlers(bot)
register_bonus_handlers(bot)
register_support_handler(bot)

# Start command
@bot.message_handler(commands=["start"])
def handle_start(message):
    show_main_menu(bot, message.chat.id)

# Launch the bot
if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.infinity_polling()
