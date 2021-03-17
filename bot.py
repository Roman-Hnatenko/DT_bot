import telebot
import random
from token_ import token_
from message_text import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

main_list = list(list_values)
bot = telebot.TeleBot(token_, parse_mode=None)
main_dict = None
dict_values = {i: 0 for i in list_values}
gen = None


def generator(l):
    global main_dict
    tmp = list(l)
    random.shuffle(tmp)
    main_dict = {i: tmp[i] for i in range(len(tmp))}
    for i in range(0, len(tmp[:int(len(tmp)/3) * 3]), 3):
        yield i, i+1, i+2


def generate_simple_keyboard(v1, v2):
    btn_1 = InlineKeyboardButton(main_dict[int(v1)], callback_data=f'{v1}_{v2}_0')
    btn_2 = InlineKeyboardButton(main_dict[int(v2)], callback_data=f'{v2}_{v1}_0')
    keyboard = InlineKeyboardMarkup().add(btn_1, btn_2)
    return keyboard


def generate_main_key_board(gen):
    value_1, value_2, value_3 = next(gen)
    # print(value_1, value_2, value_3)
    btn_1 = InlineKeyboardButton(main_dict[int(value_1)], callback_data=f'{value_1}_{value_2}_{value_3}_1')
    btn_2 = InlineKeyboardButton(main_dict[int(value_2)], callback_data=f'{value_2}_{value_1}_{value_3}_1')
    btn_3 = InlineKeyboardButton(main_dict[int(value_3)], callback_data=f'{value_3}_{value_1}_{value_2}_1')
    keyboard = InlineKeyboardMarkup().add(btn_1, btn_2, btn_3)
    return keyboard


def generate_after_rez_keyboard():
    btn_1 = InlineKeyboardButton('Пройти заново', callback_data='again')
    btn_2 = InlineKeyboardButton('Уточнити результат', callback_data=f'cont')
    keyboard = InlineKeyboardMarkup().add(btn_1, btn_2)
    return keyboard


def send_results(chat_id):
    results = 'РЕЗУЛЬТАТ:\n'
    list_d = list(dict_values.items())
    list_d.sort(key=lambda x: x[1], reverse=True)
    for i in list_d:
        l = f'{i[1]} - {i[0]}\n'
        results += l
    bot.send_message(chat_id, results, reply_markup=generate_after_rez_keyboard())


@bot.message_handler(commands=['start'])
def start(message):
    global gen
    gen = generator(main_list)
    bot.send_message(message.chat.id, start_message_2,
                           reply_markup=generate_main_key_board(gen))


def start_again(call):
    global gen
    global main_list
    main_list = list(list_values)
    gen = generator(list_values)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=generate_main_key_board(gen))


@bot.callback_query_handler(func=lambda x: True)
def callback_query(call):
    value = call.data.split('_')[-1]
    global main_dict
    global gen
    global dict_values
    print(call.data)
    if call.data == 'again':
        dict_values = {i: 0 for i in list_values}
        start_again(call)
    elif call.data == 'cont':
        start_again(call)

    elif value == '1':
        v1, v2, v3, _ = tuple(str(call.data).split('_'))

        dict_values[main_dict[int(v1)]] += 1
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=generate_simple_keyboard(v2, v3))
    else:
        v1, v2, _ = tuple(str(call.data).split('_'))
        dict_values[main_dict[int(v1)]] += 1
        main_list.pop(main_list.index(main_dict[int(v2)]))

        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=generate_main_key_board(gen))
        except StopIteration:
            try:
                gen = generator(main_list)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                              reply_markup=generate_main_key_board(gen))
            except StopIteration:
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                send_results(call.message.chat.id)

bot.polling()
