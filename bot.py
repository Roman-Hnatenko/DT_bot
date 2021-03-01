import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from itertools import combinations
from message_text import *
from token_ import token_

bot = telebot.TeleBot(token_, parse_mode=None)
start_ranking = False
list_of_choices = list()


def get_all_choices(list_of_choices):
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
    keyboard = create()
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

        bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=get_all_choices(list_of_choices), reply_markup=key_b)

        if not start_ranking:
            bot.register_next_step_handler(message, get_choice, counter, msg, keyboard)
        else:
            print('start_ranking = False')
            start_ranking = False

    except Exception:
        print('Something wrong')


def create():
    keyboard = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('Розпочати ранжування', callback_data=1000)
    keyboard.add(btn)
    return keyboard


@bot.callback_query_handler(func=lambda x: True)
def callback_query(call):
    global start_ranking
    if call.data == '1000':
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        msg = bot.send_message(call.message.chat.id, 'Розпочнемо ранжування!')
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        start_ranking = True

        for i in combinations(list_of_choices, 2):
            # bot.register_next_step_handler(None, ranking, i, msg)
            ranking(i, msg)
    else:
        if call.data in list_of_choices:
            bot.send_message(call.message.chat.id, f'Ви натиснули на {call.data}')


def generate_keyboard(i):
    first_choice = i[0]
    second_choice = i[1]
    print(first_choice, second_choice)
    btn_1 = InlineKeyboardButton(first_choice, callback_data=first_choice)
    btn_2 = InlineKeyboardButton(second_choice, callback_data=second_choice)
    keyboard = InlineKeyboardMarkup(row_width=2).add(btn_1, btn_2)
    return keyboard


def ranking(i, msg):
    chat_id = msg.chat.id
    message_id = msg.message_id,
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text= 'Вибери щось одне:', reply_markup=generate_keyboard(i))


@bot.message_handler(content_types=['text'])
def send_help_message(message):
    bot.send_message(message.chat.id, 'Розпочни вводити альтернативи командою /start👈')

bot.polling()

