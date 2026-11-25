import os
import random

import telebot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)

TASK1_BUTTON = 'Задание первого типа'
TASK2_BUTTON = 'Задание второго типа'


def read_lines(name):
    with open(os.path.join(BASE_DIR, name), encoding='utf-8') as f:
        return [line.strip() for line in f]


def load_task1():
    # zadania.txt: формулировка, затем блоки "номер + 5 слов"
    lines = read_lines('zadania.txt')
    header = lines[0]
    tasks, current = [], []
    for line in lines[1:]:
        if line.isdigit():
            if current:
                tasks.append(current)
            current = []
        elif line:
            current.append(line)
    if current:
        tasks.append(current)

    answers = [line for line in read_lines('otveti.txt') if line.isalpha()]

    explanations = {}
    number = None
    for line in read_lines('obiasnenie.txt'):
        if line.isdigit():
            number = int(line) - 1
        elif line and number is not None:
            explanations[number] = line

    n = min(len(tasks), len(answers))
    return header, tasks[:n], answers[:n], explanations


def load_task2():
    # zadka2.txt: слово с "|" перед ударной гласной
    words = []
    for line in read_lines('zadka2.txt'):
        if '|' not in line:
            continue
        before, after = line.split('|', 1)
        words.append((before + after, before + after[:1].upper() + after[1:]))
    return words


HEADER, TASKS1, ANSWERS1, EXPLANATIONS1 = load_task1()
TASKS2 = load_task2()


def normalize(text):
    return text.strip().lower().replace('ё', 'е')


def main_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(TASK1_BUTTON, TASK2_BUTTON)
    return keyboard


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    photo_path = os.path.join(BASE_DIR, 'forbotcitata.jpg')
    if os.path.exists(photo_path):
        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    bot.send_message(
        message.chat.id,
        'Привет, я - бот, созданный с целью научить тебя правилам орфоэпии, '
        'тем самым помочь тебе хорошо написать экзамен по русскому языку!',
        reply_markup=main_keyboard(),
    )


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(
        message.chat.id,
        f'{TASK1_BUTTON}: найди слово, в котором неверно выделена ударная гласная.\n'
        f'{TASK2_BUTTON}: напиши слово, выделив ударную гласную заглавной буквой.\n'
        '/stop - прервать задание.',
        reply_markup=main_keyboard(),
    )


def is_stop(message):
    return message.text in ('/stop', TASK1_BUTTON, TASK2_BUTTON)


def send_task1(message):
    i = random.randrange(len(TASKS1))
    text = HEADER + '\n' + '\n'.join(TASKS1[i])
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, 'Введите строчными буквами выбранное слово')
    bot.register_next_step_handler(message, answer_check1, i)


def answer_check1(message, i):
    if is_stop(message):
        return send_text(message)
    if normalize(message.text or '') == normalize(ANSWERS1[i]):
        bot.send_message(message.chat.id, 'Молодец, всё верно!😁✅')
        if i in EXPLANATIONS1:
            bot.send_message(message.chat.id, EXPLANATIONS1[i], reply_markup=main_keyboard())
    else:
        bot.send_message(message.chat.id, 'Неверно, попробуй ещё раз')
        bot.register_next_step_handler(message, answer_check1, i)


def send_task2(message):
    i = random.randrange(len(TASKS2))
    bot.send_message(message.chat.id, TASKS2[i][0])
    bot.send_message(message.chat.id,
                     'Введите данное слово, обозначив ударную букву заглавной, а остальные - строчными')
    bot.register_next_step_handler(message, answer_check2, i)


def answer_check2(message, i):
    if is_stop(message):
        return send_text(message)
    answer = (message.text or '').strip().replace('Ё', 'Е').replace('ё', 'е')
    correct = TASKS2[i][1].replace('Ё', 'Е').replace('ё', 'е')
    if answer == correct:
        bot.send_message(message.chat.id, 'Молодец, всё верно!😁✅', reply_markup=main_keyboard())
    elif answer.lower() != correct.lower():
        bot.send_message(message.chat.id, 'Проверь написание слова и попробуй ещё раз')
        bot.register_next_step_handler(message, answer_check2, i)
    else:
        bot.send_message(message.chat.id, 'Неверно, попробуй ещё раз')
        bot.register_next_step_handler(message, answer_check2, i)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == TASK1_BUTTON:
        send_task1(message)
    elif message.text == TASK2_BUTTON:
        send_task2(message)
    elif message.text == '/stop':
        bot.send_message(message.chat.id, 'Выбери тип задания', reply_markup=main_keyboard())
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю. Напиши /help.')


if __name__ == '__main__':
    bot.infinity_polling()
