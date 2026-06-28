import random
import threading
import time
import telebot

Token = "8969261382:AAGIBsEBbosE-L0n0O1FUUUy3EDoQUpOTkI"
bot = telebot.TeleBot(Token)

water_data = {}
reminders = {}

DAILY_GOAL = 2000


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Привет!\n\n"
        "/setreminder <часы> - установить напоминание\n"
        "/drank <ml> - добавить выпитую воду\n"
        "/status - посмотреть прогресс",
    )


@bot.message_handler(commands=["drank"])
def drank(message):
    user_id = message.chat.id

    try:
        amount = int(message.text.split()[1])

        if user_id not in water_data:
            water_data[user_id] = 0

        water_data[user_id] += amount

        bot.reply_to(
            message,
            f"Записано {amount} мл.\nВсего за день: {water_data[user_id]} мл.",
        )
    except (IndexError, ValueError):
        bot.reply_to(message, "Используйте: /drank 300")


@bot.message_handler(commands=["status"])
def status(message):
    user_id = message.chat.id

    current = water_data.get(user_id, 0)
    left = max(0, DAILY_GOAL - current)
    bot.reply_to(
        message, f"Выпито: {current} мл\nОсталось до цели: {left} мл"
    )


def reminder_loop(user_id, hours):
    while reminders.get(user_id) == hours:
        time.sleep(hours * 3600)

        if reminders.get(user_id) != hours:
            break

        try:
            bot.send_message(
                user_id, "Не забывай пить воду! Выпей стакан воды."
            )
        except Exception:
            break


@bot.message_handler(commands=["setreminder"])
def set_reminder(message):
    user_id = message.chat.id

    try:
        hours = int(message.text.split()[1])
        reminders[user_id] = hours

        thread = threading.Thread(
            target=reminder_loop, args=(user_id, hours), daemon=True
        )
        thread.start()

        bot.reply_to(message, f"Напоминание установлено каждые {hours} час(а).")
    except (IndexError, ValueError):
        bot.reply_to(message, "Используйте: /setreminder 2")


print("Бот запущен...")
bot.infinity_polling()