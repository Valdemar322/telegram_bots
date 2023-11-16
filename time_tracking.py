from datetime import date
import calendar

# date_today = date.today()
# update_date_today = date_today.strftime("%d.%m.%Y")
# first_day_of_month = calendar.monthrange(date_today.year, date_today.month)[0]
# last_day_of_month = calendar.monthrange(date_today.year, date_today.month)[-1]
#
# with_range = 7
# height_range = 5
# res = ""
# temp = 0
# date_placeholder = 1
#
# for y in range(height_range):
#     for x in range(temp, temp + with_range):
#         if x < first_day_of_month or x >= last_day_of_month + first_day_of_month:
#             res += " " + "  "
#         else:
#             res += str(date_placeholder) + "  "
#             date_placeholder += 1
#     res += "\n"
#     temp += with_range
# print(res)

import telebot
from telebot import types

API_TOKEN = '6727638499:AAEfOMi0wBOeZCpleURl9Cq1Lzr0DNcFhjc'

bot = telebot.TeleBot(API_TOKEN)

days_of_week = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]

users = []
users_with_values = {}


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    count_last_month = 0
    count_month = 0
    count_year = 0
    year = 0

    if message.from_user.id not in users:
        users.append(message.from_user.id)

    users_with_values[message.from_user.id] = {"count_last_month": count_last_month}
    calendar_markup = types.ReplyKeyboardMarkup()
    calendar_btn = types.KeyboardButton("Календарь")
    calendar_markup.add(calendar_btn)
    bot.send_message(message.chat.id, "Нажми на кнопку календарь (если хочешь ...)", reply_markup=calendar_markup)

    users_with_values[message.from_user.id] = {"count_last_month": count_last_month, "count_month": count_month,
                                               "count_year": count_year, "year": year}


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    print(users_with_values)
    if message.text == "Календарь":
        bot.delete_message(message.chat.id, message.message_id)
        markup_days = types.InlineKeyboardMarkup(row_width=len(days_of_week))
        temp_days_week = []

        date_today = date.today()
        update_date_today = date_today.strftime("%d.%m.%Y")
        first_day_of_month = calendar.monthrange(date_today.year, date_today.month)[0]
        last_day_of_month = calendar.monthrange(date_today.year, date_today.month)[-1]

        with_range = 7
        height_range = 5
        res = ""
        temp = 0
        date_placeholder = 1

        for y in range(height_range):
            for x in range(temp, temp + with_range):
                if x < first_day_of_month or x >= last_day_of_month + first_day_of_month:
                    res += " " + "-"
                else:
                    res += str(date_placeholder) + "-"
                    date_placeholder += 1
            res += "\n"
            temp += with_range

        btn_days_placeholder = []
        temp_str = ""
        for _ in res:
            temp_str += _
            if _ == "\n":
                temp_str = temp_str.rstrip()
                temp_str = temp_str[:-1]
                btn_days_placeholder.append(temp_str.split("-"))
                temp_str = ""

        for day in days_of_week:
            temp_days_week.append(types.InlineKeyboardButton(f"{day}", callback_data=f"{day}"))

        for week_num in btn_days_placeholder:
            for day_num in week_num:
                temp_days_week.append(types.InlineKeyboardButton(f"{day_num}", callback_data=f"{day_num}"))

        btn_last_month = types.InlineKeyboardButton("< (last month)", callback_data="last_month")
        btn_next_month = types.InlineKeyboardButton("(next month) >", callback_data="next_month")
        markup_days.add(*temp_days_week)
        markup_days.row(btn_last_month, btn_next_month)
        bot.send_message(message.chat.id, f"Выбери дату в календаре:\n Текущая дата: {update_date_today}",
                         reply_markup=markup_days)
        users_with_values[message.from_user.id]["count_month"] = date_today.month
        users_with_values[message.from_user.id]["year"] = date_today.year
        users_with_values[message.from_user.id]["count_last_month"] = 0
        users_with_values[message.from_user.id]["count_year"] = 0
        print(users_with_values[message.from_user.id])


@bot.callback_query_handler(func=lambda callback: True)
def month_generator(callback):
    if callback.data == "last_month":
        bot.delete_message(callback.from_user.id, callback.message.message_id)
        markup_days = types.InlineKeyboardMarkup(row_width=len(days_of_week))
        users_with_values[callback.from_user.id]["count_last_month"] += 1
        temp_days_week = []

        if users_with_values[callback.from_user.id]["count_month"] - \
                users_with_values[callback.from_user.id]["count_last_month"] < 1:
            users_with_values[callback.from_user.id]["count_year"] += 1
            users_with_values[callback.from_user.id]["count_last_month"] = 0
            users_with_values[callback.from_user.id]["count_month"] = 12
            first_day_of_month = calendar.monthrange(users_with_values[callback.from_user.id]["year"] -
                                                     users_with_values[callback.from_user.id]["count_year"],
                                                     users_with_values[callback.from_user.id]["count_month"] -
                                                     users_with_values[callback.from_user.id][
                                                         "count_last_month"])[0]
            last_day_of_month = calendar.monthrange(users_with_values[callback.from_user.id]["year"] -
                                                    users_with_values[callback.from_user.id]["count_year"],
                                                    users_with_values[callback.from_user.id]["count_month"] -
                                                    users_with_values[callback.from_user.id][
                                                        "count_last_month"])[1]
            users_with_values[callback.from_user.id]["year"] -= 1

        else:
            first_day_of_month = calendar.monthrange(users_with_values[callback.from_user.id]["year"],
                                                     users_with_values[callback.from_user.id]["count_month"] -
                                                     users_with_values[callback.from_user.id][
                                                         "count_last_month"])[0]
            last_day_of_month = calendar.monthrange(users_with_values[callback.from_user.id]["year"],
                                                    users_with_values[callback.from_user.id]["count_month"] -
                                                    users_with_values[callback.from_user.id][
                                                        "count_last_month"])[-1]

        with_range = 7
        height_range = 6
        res = ""
        temp = 0
        date_placeholder = 1

        for y in range(height_range):
            for x in range(temp, temp + with_range):
                if x < first_day_of_month or x >= last_day_of_month + first_day_of_month:
                    res += " " + "-"
                else:
                    res += str(date_placeholder) + "-"
                    date_placeholder += 1
            res += "\n"
            temp += with_range

        btn_days_placeholder = []
        temp_str = ""
        for _ in res:
            temp_str += _
            if _ == "\n":
                temp_str = temp_str.rstrip()
                temp_str = temp_str[:-1]
                btn_days_placeholder.append(temp_str.split("-"))
                temp_str = ""

        for day in days_of_week:
            temp_days_week.append(types.InlineKeyboardButton(f"{day}", callback_data=f"{day}"))

        for week_num in btn_days_placeholder:
            for day_num in week_num:
                temp_days_week.append(types.InlineKeyboardButton(f"{day_num}", callback_data=f"{day_num}"))

        btn_last_month = types.InlineKeyboardButton("< (last month)", callback_data="last_month")
        btn_next_month = types.InlineKeyboardButton("(next month) >", callback_data="next_month")
        markup_days.add(*temp_days_week)
        markup_days.row(btn_last_month, btn_next_month)

        bot.send_message(callback.message.chat.id,
                         f'Выбери дату в календаре:\n Текущая дата: {users_with_values[callback.from_user.id]["count_month"] - users_with_values[callback.from_user.id]["count_last_month"]}.{users_with_values[callback.from_user.id]["year"]}',
                         reply_markup=markup_days)

    if callback.data == "next_month":
        bot.delete_message(callback.from_user.id, callback.message.message_id)
        markup_days = types.InlineKeyboardMarkup(row_width=len(days_of_week))
        users_with_values[callback.from_user.id]["count_last_month"] -= 1
        temp_days_week = []

        if users_with_values[callback.from_user.id]["count_month"] - \
                users_with_values[callback.from_user.id]["count_last_month"] > 12:
            users_with_values[callback.from_user.id]["count_year"] -= 1
            users_with_values[callback.from_user.id]["count_last_month"] = 0
            users_with_values[callback.from_user.id]["count_month"] = 1
            first_day_of_month = calendar.monthrange(users_with_values[callback.from_user.id]["year"] -
                                                     users_with_values[callback.from_user.id]["count_year"],
                                                     users_with_values[callback.from_user.id]["count_month"] -
                                                     users_with_values[callback.from_user.id][
                                                         "count_last_month"])[0]
            last_day_of_month = calendar.monthrange(users_with_values[callback.from_user.id]["year"] -
                                                    users_with_values[callback.from_user.id]["count_year"],
                                                    users_with_values[callback.from_user.id]["count_month"] -
                                                    users_with_values[callback.from_user.id][
                                                        "count_last_month"])[1]
            users_with_values[callback.from_user.id]["year"] += 1

        else:
            first_day_of_month = calendar.monthrange(users_with_values[callback.from_user.id]["year"],
                                                     users_with_values[callback.from_user.id]["count_month"] -
                                                     users_with_values[callback.from_user.id][
                                                         "count_last_month"])[0]
            last_day_of_month = calendar.monthrange(users_with_values[callback.from_user.id]["year"],
                                                    users_with_values[callback.from_user.id]["count_month"] -
                                                    users_with_values[callback.from_user.id][
                                                        "count_last_month"])[-1]

        with_range = 7
        height_range = 6
        res = ""
        temp = 0
        date_placeholder = 1

        for y in range(height_range):
            for x in range(temp, temp + with_range):
                if x < first_day_of_month or x >= last_day_of_month + first_day_of_month:
                    res += " " + "-"
                else:
                    res += str(date_placeholder) + "-"
                    date_placeholder += 1
            res += "\n"
            temp += with_range

        btn_days_placeholder = []
        temp_str = ""
        for _ in res:
            temp_str += _
            if _ == "\n":
                temp_str = temp_str.rstrip()
                temp_str = temp_str[:-1]
                btn_days_placeholder.append(temp_str.split("-"))
                temp_str = ""

        for day in days_of_week:
            temp_days_week.append(types.InlineKeyboardButton(f"{day}", callback_data=f"{day}"))

        for week_num in btn_days_placeholder:
            for day_num in week_num:
                temp_days_week.append(types.InlineKeyboardButton(f"{day_num}", callback_data=f"{day_num}"))

        btn_last_month = types.InlineKeyboardButton("< (last month)", callback_data="last_month")
        btn_next_month = types.InlineKeyboardButton("(next month) >", callback_data="next_month")
        markup_days.add(*temp_days_week)
        markup_days.row(btn_last_month, btn_next_month)

        bot.send_message(callback.message.chat.id,
                         f'Выбери дату в календаре:\n Текущая дата: {users_with_values[callback.from_user.id]["count_month"] - users_with_values[callback.from_user.id]["count_last_month"]}.{users_with_values[callback.from_user.id]["year"]}',
                         reply_markup=markup_days)
    print(users_with_values)

bot.infinity_polling()
