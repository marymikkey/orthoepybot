import telebot
import logging
import parser
import random
from random import randint
from random import randrange
TOKEN = "1609343964:AAGtHHxr56BuGzpUssqy54lUoshLWY0LB_g"
bot = telebot.TeleBot(TOKEN)
APP_NAME = 'orthoepybot'
from telebot import types
from bs4 import BeautifulSoup
from lxml import html
import requests
@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    photo1 = open('/home/marymikkey/botik/forbotcitata.jpg', 'rb')
    bot.send_photo(message.chat.id, photo1)
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Задание первого типа', 'Задание второго типа')
    bot.send_message(message.chat.id,
                     'Привет, я - бот, созданный с целью научить тебя правилам орфоэпии, тем самым помочь тебе хорошо написать экзамен по русскому языку!',
                     reply_markup=keyboard)

answer = ''



@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Задание первого типа':
        i = randrange(0, 7)
        global c1
        c1 = i
        f = open('zadania.txt', 'r')
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]

        words = []
        for line in lines:
            if line.isalpha():
                words.append(line)

        def func_chunk(lst, n):
            for x in range(0, len(lst), n):
                e_c = lst[x: n + x]

                if len(e_c) == n:
                    e_c = e_c + [None for y in range(n - len(e_c))]
                yield e_c

        spispi = list(func_chunk(words, 5))

        taska = '\n'.join(' '.join((map(str, spispi[i]))).split())


        maintask = lines[0]
        vivod1 = maintask + '\n' + taska
        taskspis = []
        words = []

        bot.send_message(message.chat.id, vivod1)
        bot.send_message(message.chat.id, 'Введите строчными буквами выбранное слово')
        bot.register_next_step_handler(message, answer_check)
    elif message.text == 'Задание второго типа':
        u = randrange(0, 24)

        global c2
        c2 = u
        bot.send_message(message.chat.id, words2[u])
        bot.send_message(message.chat.id, 'Введите данное слово, обозначив ударную букву заглавной, а остальные - строчными')



        bot.register_next_step_handler(message, answer_check2)




#создаем список верных ответов
f1 = open('otveti.txt', 'r')
lines1 = f1.readlines()
lines1 = [line1.rstrip() for line1 in lines1]
answers = []
for line1 in lines1:
    if line1.isalpha():
        answers.append(line1)


#создаем список объяснений
f2 = open('obiasnenie.txt', 'r')
lines2 = f2.readlines()
lines2 = [line2.rstrip() for line2 in lines2]
explanations = []
for line2 in lines2:
    if not line2.isdigit():
        explanations.append(line2)





#проверкаответов1
def answer_check(message):
    answer = message.text
    if answer == answers[c1]:
        bot.send_message(message.chat.id, "Молодец, всё верно!😁✅")
        bot.send_message(message.chat.id, explanations[c1])

        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Задание первого типа', 'Задание второго типа')

    else:
        bot.send_message(message.chat.id, "Неверно, попробуй ещё раз")
        bot.register_next_step_handler(message, answer_check)
# проверкаответов2
def answer_check2(message):
    answer = message.text
    if answer == ans2[c2]:
        bot.send_message(message.chat.id, "Молодец, всё верно!😁✅")
        bot.update_listener
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Задание первого типа', 'Задание второго типа')


    else:
        bot.send_message(message.chat.id, "Неверно, попробуй ещё раз")
        bot.register_next_step_handler(message, answer_check2)
#обрабатываем список заданий 2
f3= open('zadka2.txt', 'r')
lines = f3.readlines()
lines = [line.rstrip() for line in lines]

words2 = []
ans2 = []
for line in lines:
    for word in line:
        if not word.isalpha():
            line = line.replace('|', '')
    words2.append(line)

print(words2)

#обрабат спис ответов2
linepart1 = ()
linepart2 = ()
for line in lines:
        x2 = line.find('|')+1
        linepart1 = line[: x2]
        linepart2 = line[x2 : ]
        linepart2 = linepart2.capitalize()
        line = linepart1.replace('|', '') + linepart2
        ans2.append(line)
print(ans2)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, хочешь потренироваться?")

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")










bot.polling(none_stop=True, interval=0)
