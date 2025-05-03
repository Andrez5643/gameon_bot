import telebot

BOT_TOKEN = '7575282180:AAE87kgjHJbjfSewuvr0jr9_lNGjaj811dw'
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='Markdown')

admin_username = '@KaliDapper'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
        "🎯 *Welcome to GameOn Assistance!*\n\n"
        "Your personal concierge for deposits, balances, and withdrawals.\n\n"
        "Use the menu below or type one of these:\n\n"
        "💸 /deposit – Make a deposit\n"
        "💵 /withdraw – Request a payout\n"
        "📊 /balance – Check your balance\n"
        "🧾 /howtodeposit – Step-by-step deposit guide\n"
        "📞 /support – Contact a live agent"
    )

@bot.message_handler(commands=['deposit'])
def handle_deposit(message):
    bot.send_message(message.chat.id,
        "💸 *Deposit Instructions:*\n\n"
        "Please send your funds to one of the following:\n"
        "- *CashApp:* `$GameOnCash1`\n"
        "- *Apple Pay:* `346-000-1111`\n"
        "- *Zelle:* `zelle1@example.com`\n"
        "- *BTC:* `bc1qexampleaddress1`\n\n"
        "Once sent, reply with a screenshot or message our agent: " + admin_username
    )

@bot.message_handler(commands=['howtodeposit'])
def tutorial(message):
    bot.send_message(message.chat.id,
        "🧾 *How to Deposit:*\n\n"
        "1️⃣ Use /deposit to choose your payment method.\n"
        "2️⃣ Send the amount using the info provided.\n"
        "3️⃣ Screenshot your payment.\n"
        "4️⃣ Message it here or contact " + admin_username + ".\n\n"
        "We'll confirm and credit your balance shortly!"
    )

@bot.message_handler(commands=['balance'])
def balance(message):
    bot.send_message(message.chat.id,
        "📊 *Balance Check:*\n\n"
        "Please message " + admin_username + " for your latest balance.\n"
        "We'll be adding automated balances soon 💼"
    )

@bot.message_handler(commands=['withdraw'])
def withdraw(message):
    bot.send_message(message.chat.id,
        "💵 *Withdrawal Request:*\n\n"
        "To cash out, message " + admin_username + " with:\n"
        "- Your username\n"
        "- Amount\n"
        "- Preferred payment method\n\n"
        "We'll process ASAP. ✅"
    )

@bot.message_handler(commands=['support'])
def support(message):
    bot.send_message(message.chat.id,
        "📞 *Need Help?*\n\n"
        "Message our support agent directly: " + admin_username + "\n"
        "We're here 24/7 to help!"
    )

print("🚀 GameOn Assistance Bot is running...")
bot.infinity_polling()
import telebot

# ✅ Use your actual token
BOT_TOKEN = '7575282180:AAE87kgjHJbjfSewuvr0jr9_lNGjaj811dw'
bot = telebot.TeleBot(BOT_TOKEN)

# ✅ Basic /start command to confirm bot is alive
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to GameOn! Use /deposit, /balance, or /support.")

# ✅ Dummy deposit command
@bot.message_handler(commands=['deposit'])
def handle_deposit(message):
    bot.send_message(message.chat.id, "💸 Please send payment via CashApp to $GameOnCash1 and reply with screenshot.")

# ✅ Dummy support command
@bot.message_handler(commands=['support'])
def support(message):
    bot.send_message(message.chat.id, "📞 For support, contact @KaliDapper")

# ✅ Start the bot
print("✅ Bot is running. Waiting for messages...")
bot.infinity_polling()

