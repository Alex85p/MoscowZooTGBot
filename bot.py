import telebot
from telebot import types
from config import TOKEN
from event import get_questions

bot = telebot.TeleBot(TOKEN)

# Переменная для хранения текущего вопроса
current_question = 0

# Переменная для хранения счета очков
scores = {
    'Option 1': 0,
    'Option 2': 0
}

# Создание меню
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Event')
item2 = types.KeyboardButton('Contacts')
item3 = types.KeyboardButton('Help')
item4 = types.KeyboardButton('About')

markup.add(item1, item2, item3, item4)
description = "Привет! Я бот. Я здесь, чтобы помочь тебе. Выбери один из пунктов меню ниже:"
event = 'Ответь на несколько вопросов, чтобы узнать свое тотемное животное!'


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, description, reply_markup=markup)


# Обработчик нажатия кнопки "Event"
@bot.message_handler(func=lambda message: message.text == 'Event')
def handle_event(message):
    bot.send_message(message.chat.id, event)
    global current_question
    global scores
    global answers
    current_question = 0
    scores = {
        'Option 1': 0,
        'Option 2': 0
    }
    answers = {}
    send_question(message.chat.id)


# Переменная для хранения ответов на вопросы
answers = {}


# Функция для обновления ответа пользователя
def update_answer(chat_id, question, answer):
    if chat_id not in answers:
        answers[chat_id] = {}
    answers[chat_id][question] = answer


# Функция для отправки вопроса и вариантов ответов
def send_question(chat_id):
    global current_question
    questions = get_questions()
    if current_question < len(questions):
        question = questions[current_question][0]
        option1 = questions[current_question][1]
        option2 = questions[current_question][2]

        # Создание списка кнопок вариантов ответов
        inline_buttons = [
            types.InlineKeyboardButton(text=option1, callback_data=f'1_{current_question}'),
            types.InlineKeyboardButton(text=option2, callback_data=f'2_{current_question}')
        ]

        # Установка предыдущих кнопок в неактивное состояние
        if current_question > 0:
            previous_question = questions[current_question - 1][0]
            previous_answer = answers.get(chat_id, {}).get(previous_question)
            if previous_answer:
                for button in inline_buttons:
                    if button.callback_data.startswith(previous_answer):
                        button.is_disabled = True

        # Создание объекта клавиатуры с кнопками вариантов ответов
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*inline_buttons)

        bot.send_message(chat_id, f'Вопрос: {question}', reply_markup=keyboard)
    else:
        bot.send_message(chat_id, 'Вопросы закончились. Результаты:')
        for option, score in scores.items():
            bot.send_message(chat_id, f'{option}: {score}')
        # Создание кнопки рестарта
        restart_button = types.InlineKeyboardButton('Рестарт', callback_data='restart')

        # Создание клавиатуры с кнопкой рестарта
        restart_markup = types.InlineKeyboardMarkup()
        restart_markup.add(restart_button)

        bot.send_message(chat_id, 'Желаете сыграть еще раз?', reply_markup=restart_markup)


# Обработчик нажатий на кнопки с вариантами ответов
@bot.callback_query_handler(func=lambda call: call.data.startswith(('1_', '2_')))
def handle_answer(call):
    global current_question
    global scores
    questions = get_questions()
    if current_question < len(questions):
        question = questions[current_question][0]
        answer, question_index = call.data.split('_')
        question_index = int(question_index)

        chat_id = call.message.chat.id

        # Проверка, был ли уже дан ответ на этот вопрос
        if chat_id not in answers or question not in answers[chat_id]:
            if question_index == current_question:
                # Обновление ответа пользователя
                update_answer(chat_id, question, answer)

                scores['Option ' + answer] += 1
                current_question += 1
                send_question(chat_id)
            else:
                bot.answer_callback_query(call.id, text='Вы уже ответили на этот вопрос')
        else:
            bot.answer_callback_query(call.id, text='Вы уже ответили на этот вопрос')
    else:
        bot.answer_callback_query(call.id)


# Обработчик нажатия на кнопку рестарта
@bot.callback_query_handler(func=lambda call: call.data == 'restart')
def handle_restart(call):
    restart_quiz(call.message.chat.id)  # Запускаем новую сессию викторины


# Функция для перезапуска викторины
def restart_quiz(chat_id):
    global current_question
    global scores
    current_question = 0
    scores = {
        'Option 1': 0,
        'Option 2': 0
    }
    answers.pop(chat_id, None)  # Удаляем предыдущие ответы пользователя
    send_question(chat_id)


bot.polling()
