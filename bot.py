import telebot
import random
from itertools import combinations
import matplotlib.pyplot as plt

import keyboards
from message_text import *
from token_ import token_

bot = telebot.TeleBot(token_, parse_mode=None)

start_ranking = False
list_of_choices = list()
msg_id = None
chat_id = None
gen = None


def generator():
    tmp = [i for i in combinations(list_of_choices, 2)]
    random.shuffle(tmp)
    flag = True
    for i in tmp:
        if flag:
            yield i
        else:
            j = (i[1], i[0])
            yield j
        flag = not flag


def get_all_choices():
    result = 'Добавлені альтернативи:\n'
    for choices in list_of_choices:
        choices = choices[0].upper() + choices[1:]
        result += choices + '\n'
    return result


@bot.message_handler(commands=['start'])
def start(message):
    bot.disable_save_next_step_handlers()
    counter = 0
    msg = bot.send_message(message.chat.id, start_message)
    keyboard = keyboards.end_input()
    bot.register_next_step_handler(message, get_choice, counter, msg, keyboard)


def get_choice(message, counter, msg, keyboard):
    global start_ranking
    global list_of_choices
    counter += 1

    try:
        key_b = keyboard if counter > 2 else None
        choice = message.text[0].upper() + message.text[1:]
        # if choice not in list_of_choices:
        list_of_choices.append(choice)

        bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=get_all_choices(), reply_markup=key_b)

        if not start_ranking:
            bot.register_next_step_handler(message, get_choice, counter, msg, keyboard)
        else:
            print('start_ranking = False')
            start_ranking = False

    except Exception:
        print('Something wrong')


@bot.callback_query_handler(func=lambda x: True)
def callback_query(call):
    global msg_id
    global chat_id
    global start_ranking
    global gen
    if call.data == '1000':
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        msg = bot.send_message(call.message.chat.id, 'Розпочнемо ранжування!')
        gen = generator()
        chat_id = msg.chat.id
        msg_id = msg.message_id

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        start_ranking = True
        ranking(gen)

    else:
        if call.data in list_of_choices:

            bot.send_message(call.message.chat.id, f'Ви натиснули на {call.data}')
            ranking(gen)


def ranking(gen):
    try:
        bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=keyboards.binary_keyboard(gen))
    except StopIteration:
        bot.edit_message_reply_markup(chat_id, msg_id)


@bot.message_handler(content_types=['text'])
def send_help_message(message):
    bot.send_message(message.chat.id, 'Розпочни вводити альтернативи командою /start👈')


bot.polling()

