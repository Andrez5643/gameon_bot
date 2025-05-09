from threading import Timer

# Keeps track of active timers per user
expiration_timers = {}

def start_expiration_timer(bot, chat_id, method):
    if chat_id in expiration_timers:
        expiration_timers[chat_id].cancel()

    def notify_expiring(time_left):
        bot.send_message(chat_id, f"⏰ Address will expire in less than {time_left} minutes. If it does expire, do NOT send there anymore. Thanks.")

    def expire():
        bot.send_message(chat_id, "❌ This address has expired. Please request a new one before sending.")
        expiration_timers.pop(chat_id, None)

    # Notify 10, 5, and 1 minute before expiration
    Timer(20 * 60, lambda: notify_expiring(10)).start()
    Timer(25 * 60, lambda: notify_expiring(5)).start()
    Timer(29 * 60, lambda: notify_expiring(1)).start()

    # Expire after 30 minutes
    t = Timer(30 * 60, expire)
    t.start()
    expiration_timers[chat_id] = t
