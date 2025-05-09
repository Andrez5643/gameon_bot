from telebot.types import Message
import os

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "@GameOnAdmin")

def register_group_command(bot):
    @bot.message_handler(commands=["create_group"])
    def handle_create_group(message: Message):
        if message.from_user.username != ADMIN_USERNAME.lstrip("@"):
            bot.reply_to(message, "❌ You are not authorized to use this command.")
            return

        try:
            args = message.text.split(maxsplit=1)
            if len(args) != 2:
                bot.reply_to(message, "⚠️ Usage: /create_group [Sportsbook Username]")
                return

            username = args[1]
            group_title = f"Game On | {username}"
            chat = bot.create_chat(title=group_title, members=[message.from_user.id])
            bot.send_message(chat.id, f"✅ Private group created for {username}.")
        except Exception as e:
            print("❌ Failed to create group:", e)
            bot.reply_to(message, "❌ Something went wrong creating the group.")
