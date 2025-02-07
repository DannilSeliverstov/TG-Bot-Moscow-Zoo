import os
from telebot import types
from config import IMAGE_FOLDER
import random


def get_questions():
    questions = [
        {
            "question": "Как вы предпочитаете проводить свободное время?",
            "answers": {
                "Активно, занимаясь спортом или путешествуя.": "Амурский тигр",
                "Спокойно, читая книгу или смотря фильм.": "Дикдик",
                "На природе, гуляя в лесу или парке.": "Капибара",
                "В компании друзей, весело проводя время.": "Африканская Соня",
                "Всё время делая что-то полезное.": "Бобр"
            },
        },
        {
            "question": "Какой климат вам больше по душе?",
            "answers": {
                "Холодный и снежный.": "Амурский тигр",
                "Теплый и солнечный.": "Капибара",
                "Влажный и прохладный.": "Африканская Соня",
                "Засушливый и жаркий.": "Дикдик",
                "Согласен на любой, если есть водоемы.": "Бобр"
            },
        },
        {
            "question": "Как бы вы описали свой характер?",
            "answers": {
                "Смелый, решительный, я всегда добиваюсь своего.": "Амурский тигр",
                "Тихий и незаметный, мне нравится быть в одиночестве.": "Дикдик",
                "Спокойный и доброжелательный, люблю мир и природу.": "Капибара",
                "Общительный и веселый, люблю играть и смеяться.": "Африканская Соня",
                "Целеустремленный и трудолюбивый, всегда нахожу решение.": "Бобр"
            },
        },
        {
            "question": "Какой образ жизни вам ближе?",
            "answers": {
                "Я предпочитаю независимость и одиночество.": "Амурский тигр",
                "Я живу в стаде, мне нравится общение с другими.": "Дикдик",
                "Я предпочитаю быть в окружении друзей и природы.": "Капибара",
                "Я люблю быть в центре внимания, но не против провести время в тени.": "Африканская Соня",
                "Я трудолюбив, мне нравится строить и создавать.": "Бобр"
            },
        },
        {
            "question": "Какой вид пищи вам больше всего нравится?",
            "answers": {
                "Я хищник, предпочитаю мясо.": "Амурский тигр",
                "Я люблю разнообразие, в том числе фрукты и зелень.": "Капибара",
                "Я предпочитаю что-то лёгкое и сладкое.": "Африканская Соня",
                "Я питаюсь травой и листьями, это моё основное питание.": "Дикдик",
                "Мне нравятся водные растения и древесина.": "Бобр"
            },
        }
    ]

    for question in questions:
        answer_items = list(question["answers"].items())
        random.shuffle(answer_items)
        question["answers"] = dict(answer_items)

    random.shuffle(questions)

    return questions


def get_result(answers):
    if not answers:
        return "Не удалось определить тотемное животное 😢"

    result_count = {}
    for answer in answers:
        result_count[answer] = result_count.get(answer, 0) + 1
    return max(result_count, key=result_count.get)


def get_image_path(animal_name):
    image_path = os.path.join(IMAGE_FOLDER, f"{animal_name}.jpeg")

    if os.path.exists(image_path):
        return image_path
    return None


def create_restart_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Попробовать еще раз"))
    markup.add(types.KeyboardButton("Связаться с сотрудником"))
    markup.add(types.KeyboardButton("Поделиться с друзьями"))
    return markup
