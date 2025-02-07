import telebot
from telebot import types
from config import TOKEN, GUARDIANSHIP_LINK, SUPPORT_EMAIL, SUPPORT_PHONE, BOT_SHARE_LINK
from extensions import get_questions, get_result, get_image_path, create_restart_markup
import os

bot = telebot.TeleBot(TOKEN)
questions = get_questions()
user_answers = {}


@bot.message_handler(commands=['start'])
def start_quiz(message):
    user_answers[message.chat.id] = []
    bot.send_message(
        message.chat.id,
        "Привет! Пройди викторину, чтобы узнать, какое животное будет твоим тотемом. Начнем?"
    )
    ask_question(message.chat.id, 0)


def ask_question(chat_id, index):
    if index < len(questions):
        question = questions[index]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        for answer in question["answers"].keys():
            markup.add(types.KeyboardButton(answer))

        bot.send_message(chat_id, question["question"], reply_markup=markup)
    else:
        result = get_result(user_answers[chat_id])
        image_path = get_image_path(result)

        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as img:
                bot.send_photo(chat_id, img)

        bot.send_message(
            chat_id,
            f"Твоё тотемное животное — {result}!",
            reply_markup=create_restart_markup()
        )
        bot.send_message(
            chat_id,
            f"Узнать больше об опеке: {GUARDIANSHIP_LINK}",
            disable_web_page_preview=True
        )


@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    chat_id = message.chat.id

    if chat_id not in user_answers:
        start_quiz(message)
        return

    for question in questions:
        if message.text in question["answers"]:
            user_answers[chat_id].append(question["answers"][message.text])
            index = len(user_answers[chat_id])
            ask_question(chat_id, index)
            return

    if message.text == "Попробовать еще раз":
        start_quiz(message)
        return

    if message.text == "Связаться с сотрудником":
        result = get_result(user_answers.get(chat_id, []))
        bot.send_message(
            chat_id,
            f"Вы можете связаться с нашим сотрудником:\n📧 {SUPPORT_EMAIL}\n📞 {SUPPORT_PHONE}\nВаш результат: {result}"
        )
        return

    if message.text == "Поделиться с друзьями":
        if chat_id in user_answers and user_answers[chat_id]:
            result = get_result(user_answers[chat_id])
        else:
            bot.send_message(chat_id, "Сначала пройдите тест, чтобы узнать своё тотемное животное!")
            return

        share_text = f"Моё тотемное животное — {result}! Узнай своё тотемное животное в боте: {BOT_SHARE_LINK}"
        bot.send_message(chat_id, share_text)
        return


if __name__ == "__main__":
    bot.polling(none_stop=True)
