import telebot
import random
from token_ import token_
from message_text import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from itertools import combinations

bot = telebot.TeleBot(token_, parse_mode=None)
main_dict = {i: list_values[i] for i in range(len(list_values))}
dict_values = {i: 0 for i in list_values}


def generator():
    global dict_values
    tmp = [i for i in combinations(range(len(dict_values)), 3)]
    random.shuffle(tmp)
    for i in tmp:
        l_i = list(i)
        random.shuffle(l_i)
        yield l_i


gen = generator()


def generate_simple_keyboard(v1, v2):
    btn_1 = InlineKeyboardButton(main_dict[int(v1)], callback_data=f'{v1}_{v2}_0')
    btn_2 = InlineKeyboardButton(main_dict[int(v2)], callback_data=f'{v2}_{v1}_0')
    keyboard = InlineKeyboardMarkup().add(btn_1, btn_2)
    return keyboard


def generate_main_key_board(gen):
    value_1, value_2, value_3 = next(gen)
    btn_1 = InlineKeyboardButton(main_dict[int(value_1)], callback_data=f'{value_1}_{value_2}_{value_3}_1')
    btn_2 = InlineKeyboardButton(main_dict[int(value_2)], callback_data=f'{value_2}_{value_1}_{value_3}_1')
    btn_3 = InlineKeyboardButton(main_dict[int(value_3)], callback_data=f'{value_3}_{value_1}_{value_2}_1')
    keyboard = InlineKeyboardMarkup().add(btn_1, btn_2, btn_3)
    return keyboard


def send_results(chat_id):
    results = 'Результат:\n'
    list_d = list(dict_values.items())
    list_d.sort(key=lambda x: x[1], reverse=True)
    for i in list_d:
        l = f'{i[0]} - {i[1]}\n'
        results += l
    bot.send_message(chat_id, results)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, start_message_2,
                           reply_markup=generate_main_key_board(gen))


@bot.callback_query_handler(func=lambda x: True)
def callback_query(call):
    value = call.data.split('_')[-1]
    global main_dict
    global gen
    if value == '1':
        v1, v2, v3, _ = tuple(str(call.data).split('_'))

        dict_values[main_dict[int(v1)]] += 2
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=generate_simple_keyboard(v2, v3))
    else:
        v1, v2, _ = tuple(str(call.data).split('_'))
        dict_values[main_dict[int(v1)]] += 1

        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=generate_main_key_board(gen))
        except StopIteration:

            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            send_results(call.message.chat.id)


bot.polling()