from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.sheets import log_bonus_claim, get_bonus_percent
from utils.bonus_checker import has_claimed_bonus

def register_bonus_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "bonus")
    def send_bonus_offer(call):
        user_id = call.from_user.id
        username = call.from_user.username or "N/A"
        first_name = call.from_user.first_name or "User"

        if has_claimed_bonus(user_id):
            bot.answer_callback_query(call.id, "🚫 Bonus already claimed — check back for new offers!", show_alert=True)
            return

        bonus_percent = get_bonus_percent()
        claim_text = (
            f"🎁 *Free Bonus Available!*\n"
            f"Tap below to instantly claim your bonus — no deposit needed.\n"
            f"🟡 _Limited time offer_\n\n"
            f"🔢 *Current Bonus:* {bonus_percent:.0f}%\n"
            f"👇"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🎯 Claim Bonus 🟢", callback_data="claim_bonus"))
        bot.send_message(call.message.chat.id, claim_text, reply_markup=markup, parse_mode="Markdown")

    @bot.callback_query_handler(func=lambda call: call.data == "claim_bonus")
    def claim_bonus(call):
        user_id = call.from_user.id
        username = call.from_user.username or "N/A"
        first_name = call.from_user.first_name or "User"

        if has_claimed_bonus(user_id):
            bot.answer_callback_query(call.id, "🚫 Bonus already claimed — check back for new offers!", show_alert=True)
            return

        log_bonus_claim(user_id, username, first_name)
        bot.answer_callback_query(call.id, "✅ Bonus claimed! It will be applied shortly.", show_alert=True)
        bot.send_message(call.message.chat.id, "🎉 Bonus successfully claimed! Check your account or ask your agent to confirm your credit.")

def handle_bonus(bot):
    register_bonus_handlers(bot)

