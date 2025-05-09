def register_support_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "support")
    def handle_support(call):
        support_text = (
            "🆘 *Need help?*\n\n"
            "Someone from *Game On Support* will be with you shortly.\n"
            "Feel free to reply here with your question in the meantime."
        )
        bot.send_message(call.message.chat.id, support_text, parse_mode="Markdown")
