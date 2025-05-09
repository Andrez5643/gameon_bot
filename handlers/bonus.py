from utils.sheets import log_bonus_to_sheet, has_claimed_bonus

def register_bonus_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "claim_bonus")
    def handle_bonus_claim(call):
        user_id = call.from_user.id
        first_name = call.from_user.first_name
        username = call.from_user.username or "N/A"

        if has_claimed_bonus(user_id):
            bot.send_message(call.message.chat.id,
                f"❌ Sorry {first_name}, our records show you’ve already claimed your bonus.")
        else:
            log_bonus_to_sheet(user_id, username, first_name)
            bot.send_message(call.message.chat.id,
                f"🎁 Bonus successfully claimed, {first_name}! Check your account or DM your rep if not applied.")
