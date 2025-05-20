import os
import telebot
from handlers.deposit import register_deposit_handlers, register_how_to_deposit_handler
from handlers.withdraw impot register_withdraw_handlers
from handlers.bonus import handle_bonus
from handlers.support import register_support_handler
from commands.create_group import register_group_command
from utils.menu import show_main_menu

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# Register all handlers
register_deposit_handlers(bot)
register_how_to_deposit_handler(bot)
register_withdraw_handlers(bot)
handle_bonus(bot)
register_support_handler(bot)
register_group_command(bot)

# Start command
@bot.message_handler(commands=["start"])
def handle_start(message):
    show_main_menu(bot, message.chat.id)

# Launch the bot
if __name__ == "__main__":
    print("✅ Bot is running...")
    bot.infinity_polling()
