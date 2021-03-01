from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from itertools import combinations


def generator():
    for i in combinations(list_of_choices, 2):
        yield i


def binary_keyboard():
    first_choice, second_choice = next(generator())
    print(first_choice, second_choice)
    btn_1 = InlineKeyboardButton(first_choice, callback_data=first_choice)
    btn_2 = InlineKeyboardButton(second_choice, callback_data=second_choice)
    keyboard = InlineKeyboardMarkup(row_width=2).add(btn_1, btn_2)
    return keyboard


def end_input():
    keyboard = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('Розпочати ранжування', callback_data=1000)
    keyboard.add(btn)
    return keyboard

