def register_support_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "support")
    def handle_support(call):
        chat_id = call.message.chat.id
        bot.send_message(chat_id,
            "🆘 Need help?\n\n"
            "📩 Message your rep directly at [@GameOnHost](https://t.me/GameOnHost)\n"
            "or reply here and someone will respond ASAP.",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
