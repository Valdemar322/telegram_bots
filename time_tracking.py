from datetime import date
import calendar
import telebot
from telebot import types
import re

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
    name = ""
    lastname = ""

    bot.send_message(message.chat.id, f"Привет {message.chat.username}!")
    bot.send_message(message.chat.id, f"Введите свое реальное имя:")

    users_with_values[message.from_user.id] = {"count_last_month": count_last_month, "count_month": count_month,
                                               "count_year": count_year, "year": year, "day": 0,
                                               "logical_name_var": True,
                                               "logical_lastname_var": False, "name": name, "lastname": lastname,
                                               "message_id": message.message_id, "marked_days": set(), "hour_worked": 0,
                                               "hour_worked_trigger": False, "date_message_id": [], "hour": 0,
                                               "minute": 0, "date": "", "huita": set(), "first_initializtion": True,
                                               "logical_hour_var": 0, "logical_minute_var": 0}


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if users_with_values[message.from_user.id]["logical_name_var"]:
        if users_with_values[message.from_user.id]["first_initializtion"]:
            users_with_values[message.chat.id]["huita"].add(users_with_values[message.from_user.id]["message_id"])
            users_with_values[message.chat.id]["huita"].add(users_with_values[message.from_user.id]["message_id"] + 1)
            users_with_values[message.chat.id]["huita"].add(users_with_values[message.from_user.id]["message_id"] + 2)
            users_with_values[message.from_user.id]["first_initializtion"] = False
        users_with_values[message.from_user.id]["message_id"] = message.message_id
        users_with_values[message.chat.id]["test"] = message.message_id
        users_with_values[message.from_user.id]["name"] = message.text
        users_with_values[message.from_user.id]["logical_name_var"] = False
        bot.send_message(message.chat.id, f"Введите свою реальную фамилию:")
        users_with_values[message.from_user.id]["logical_lastname_var"] = True

    elif users_with_values[message.from_user.id]["logical_lastname_var"]:
        markup_username = types.InlineKeyboardMarkup(row_width=2)
        yes_btn = types.InlineKeyboardButton("Да", callback_data="yes")
        no_btn = types.InlineKeyboardButton("Нет", callback_data="no")
        markup_username.add(yes_btn, no_btn)
        users_with_values[message.from_user.id]["lastname"] = message.text
        users_with_values[message.from_user.id]["logical_lastname_var"] = False
        bot.send_message(message.chat.id,
                         f"Перепроверьте пожалуйста правильно ли вы ввели свои данные! (это очень важно)")
        bot.send_message(message.chat.id,
                         f'Ваше имя: {users_with_values[message.from_user.id]["name"]}\nВаша фамилия: '
                         f'{users_with_values[message.from_user.id]["lastname"]}')
        bot.send_message(message.chat.id,
                         f"Ваши данные верны?\n\n(Если данные верны, нажмите кнопку 'Да'\n"
                         f"Если вы случайно опечатались и данные не верны то нажмите кнопку 'Нет')",
                         reply_markup=markup_username)

    elif message.text == "Календарь":
        for huy in users_with_values[message.chat.id]["huita"]:
            bot.delete_message(message.chat.id, huy)
        tmp_messages_id = message.message_id

        while tmp_messages_id >= users_with_values[message.from_user.id]["message_id"]:
            bot.delete_message(message.chat.id, tmp_messages_id)
            tmp_messages_id -= 1

        date_today = date.today()
        users_with_values[message.from_user.id]["count_month"] = date_today.month
        users_with_values[message.from_user.id]["year"] = date_today.year
        users_with_values[message.from_user.id]["count_last_month"] = 0
        users_with_values[message.from_user.id]["count_year"] = 0
        users_with_values[message.chat.id]["date_message_id"] = []
        calendar_call(message.chat.id)


    elif users_with_values[message.chat.id]["logical_hour_var"]:
        pattern = r"^(0?[0-9]|1[0-9]|2[0-4])$"
        if re.match(pattern, message.text) and message.text != "24":
            users_with_values[message.chat.id]["hour"] = message.text
            users_with_values[message.chat.id]["date_message_id"].append(message.message_id)
            users_with_values[message.chat.id]["logical_hour_var"] = False
            tmp_hour_id = bot.send_message(message.chat.id, "Введите количество минут: ")
            users_with_values[message.chat.id]["date_message_id"].append(tmp_hour_id.message_id)
            users_with_values[message.chat.id]["logical_minute_var"] = True

        elif message.text == "24":
            users_with_values[message.chat.id]["hour"] = message.text
            users_with_values[message.chat.id]["date_message_id"].append(message.message_id)
            users_with_values[message.chat.id]["logical_hour_var"] = False
            markup_data = types.InlineKeyboardMarkup()
            true_data_record = types.InlineKeyboardButton("Запись времени", callback_data="true_data_record")
            false_data_record = types.InlineKeyboardButton("Я-крабик", callback_data="false_data_record")
            markup_data.row(true_data_record, false_data_record)
            tmp_time_id = bot.send_message(message.chat.id, f'Пожалуйста перепроверьте ваши данные, а именно:\n'
                                                            f'Количество часов: {users_with_values[message.chat.id]["hour"]}'
                                                            f'\nКоличество минут: {users_with_values[message.chat.id]["minute"]}'
                                                            f'\nЗа {users_with_values[message.chat.id]["date"]}'
                                                            f'\nЕсли данные верны нажмите кнопку: "Запись времени"'
                                                            f'\nЕсли данные не верны нажмите кнопку: "Я-крабик"',
                                           reply_markup=markup_data)
            users_with_values[message.chat.id]["date_message_id"].append(tmp_time_id.message_id)

        else:
            users_with_values[message.chat.id]["date_message_id"].append(message.message_id)
            temp_msg = bot.send_message(message.chat.id,
                                        "Вы ввели некорректное значение! Введите количество часов в диапазоне от 0 до 24 (включительно)")
            users_with_values[message.chat.id]["date_message_id"].append(temp_msg.message_id)


    elif users_with_values[message.chat.id]["logical_minute_var"]:
        pattern = r"^[0-5]?[0-9]$"
        if re.match(pattern, message.text):
            users_with_values[message.chat.id]["minute"] = message.text
            users_with_values[message.chat.id]["date_message_id"].append(message.message_id)
            users_with_values[message.chat.id]["logical_minute_var"] = False
            markup_data = types.InlineKeyboardMarkup()
            true_data_record = types.InlineKeyboardButton("Запись времени ✍️", callback_data="true_data_record")
            false_data_record = types.InlineKeyboardButton("Я-крабик 🦀", callback_data="false_data_record")
            markup_data.row(true_data_record, false_data_record)
            tmp_time_id = bot.send_message(message.chat.id, f'Пожалуйста перепроверьте ваши данные, а именно:\n'
                                                            f'Количество часов: {users_with_values[message.chat.id]["hour"]}'
                                                            f'\nКоличество минут: {users_with_values[message.chat.id]["minute"]}'
                                                            f'\nЗа {users_with_values[message.chat.id]["date"]}'
                                                            f'\nЕсли данные верны нажмите кнопку: "Запись времени"'
                                                            f'\nЕсли данные не верны нажмите кнопку: "Я-крабик"',
                                           reply_markup=markup_data)
            users_with_values[message.chat.id]["date_message_id"].append(tmp_time_id.message_id)

        else:
            users_with_values[message.chat.id]["date_message_id"].append(message.message_id)
            temp_msg = bot.send_message(message.chat.id,
                                        "Вы ввели некорректное значение! Введите количество минут в диапазоне от 0 до 59 (включительно)")
            users_with_values[message.chat.id]["date_message_id"].append(temp_msg.message_id)

    else:
        users_with_values[message.chat.id]["date_message_id"].append(message.message_id)


def calendar_month_range(user_id):
    first_day_of_month = calendar.monthrange(users_with_values[user_id]["year"] -
                                             users_with_values[user_id]["count_year"],
                                             users_with_values[user_id]["count_month"] -
                                             users_with_values[user_id][
                                                 "count_last_month"])[0]
    last_day_of_month = calendar.monthrange(users_with_values[user_id]["year"] -
                                            users_with_values[user_id]["count_year"],
                                            users_with_values[user_id]["count_month"] -
                                            users_with_values[user_id][
                                                "count_last_month"])[1]
    return {"first_day_of_month": first_day_of_month, "last_day_of_month": last_day_of_month}


def calendar_call(user_id):
    markup_days = types.InlineKeyboardMarkup(row_width=len(days_of_week))
    temp_days_week = []

    if users_with_values[user_id]["count_month"] - \
            users_with_values[user_id]["count_last_month"] > 12:
        users_with_values[user_id]["count_year"] -= 1
        users_with_values[user_id]["count_last_month"] = 0
        users_with_values[user_id]["count_month"] = 1
        first_day_of_month = calendar_month_range(user_id)["first_day_of_month"]
        last_day_of_month = calendar_month_range(user_id)["last_day_of_month"]

    elif users_with_values[user_id]["count_month"] - \
            users_with_values[user_id]["count_last_month"] < 1:
        users_with_values[user_id]["count_year"] += 1
        users_with_values[user_id]["count_last_month"] = 0
        users_with_values[user_id]["count_month"] = 12
        first_day_of_month = calendar_month_range(user_id)["first_day_of_month"]
        last_day_of_month = calendar_month_range(user_id)["last_day_of_month"]

    else:
        first_day_of_month = calendar_month_range(user_id)["first_day_of_month"]
        last_day_of_month = calendar_month_range(user_id)["last_day_of_month"]

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

    month = users_with_values[user_id]["count_month"] - \
            users_with_values[user_id][
                "count_last_month"]
    year = users_with_values[user_id]["year"] - users_with_values[user_id]["count_year"]

    for week_num in btn_days_placeholder:
        for day_num in week_num:
            data = f"{day_num}.{month}.{year}"
            if data in users_with_values[user_id]["marked_days"]:
                temp_days_week.append(types.InlineKeyboardButton(f"📌{day_num}", callback_data=data))
            else:
                temp_days_week.append(types.InlineKeyboardButton(f"{day_num}", callback_data=data))

    btn_last_month = types.InlineKeyboardButton("< (Прошлый месяц)", callback_data="last_month")
    btn_next_month = types.InlineKeyboardButton("(Следующий месяц) >", callback_data="next_month")
    markup_days.add(*temp_days_week)
    markup_days.row(btn_last_month, btn_next_month)
    bot.send_message(user_id,
                     f'Выбери дату в календаре:\n Текущая дата: {month}.{year}',
                     reply_markup=markup_days)


@bot.callback_query_handler(func=lambda callback: True)
def month_generator(callback):
    if callback.data == "yes":
        calendar_markup = types.ReplyKeyboardMarkup()
        calendar_btn = types.KeyboardButton("Календарь")
        calendar_markup.add(calendar_btn)
        bot.send_message(callback.message.chat.id,
                         "Нажмите на кнопку Календарь для выбора даты отработанного вами дня!",
                         reply_markup=calendar_markup)

    elif callback.data == "no":
        t = callback.message.message_id
        while t >= users_with_values[callback.message.chat.id]["test"]:
            bot.delete_message(callback.message.chat.id, t)
            t -= 1
        for tmp_messages_id in users_with_values[callback.from_user.id]["date_message_id"]:
            bot.delete_message(callback.message.chat.id, tmp_messages_id)
        users_with_values[callback.from_user.id]["date_message_id"] = []
        users_with_values[callback.from_user.id]["logical_name_var"] = True

    elif callback.data == "last_month":
        bot.delete_message(callback.from_user.id, callback.message.message_id)
        if users_with_values[callback.from_user.id]["date_message_id"]:
            for tmp_messages_id in users_with_values[callback.from_user.id]["date_message_id"]:
                bot.delete_message(callback.message.chat.id, tmp_messages_id)
            users_with_values[callback.from_user.id]["date_message_id"] = []

        users_with_values[callback.from_user.id]["count_last_month"] += 1
        calendar_call(callback.from_user.id)

    elif callback.data == "next_month":
        bot.delete_message(callback.from_user.id, callback.message.message_id)
        if users_with_values[callback.from_user.id]["date_message_id"]:
            for tmp_messages_id in users_with_values[callback.from_user.id]["date_message_id"]:
                bot.delete_message(callback.message.chat.id, tmp_messages_id)
            users_with_values[callback.from_user.id]["date_message_id"] = []
        users_with_values[callback.from_user.id]["count_last_month"] -= 1
        calendar_call(callback.from_user.id)

    elif callback.data == "true_data_record":
        users_with_values[callback.from_user.id]["marked_days"].add(users_with_values[callback.from_user.id]["date"])
        users_with_values[callback.from_user.id]["date_message_id"].append(
            users_with_values[callback.from_user.id]["date_message_id"][0] - 1)
        if users_with_values[callback.from_user.id]["date_message_id"]:
            for tmp_messages_id in users_with_values[callback.from_user.id]["date_message_id"]:
                bot.delete_message(callback.message.chat.id, tmp_messages_id)
            users_with_values[callback.from_user.id]["date_message_id"] = []
        calendar_call(callback.from_user.id)

    elif callback.data == "false_data_record":
        if users_with_values[callback.from_user.id]["date_message_id"]:
            for tmp_messages_id in users_with_values[callback.from_user.id]["date_message_id"]:
                bot.delete_message(callback.message.chat.id, tmp_messages_id)
            users_with_values[callback.from_user.id]["date_message_id"] = []

    else:
        if callback.data[0] != " " and len(callback.data) > 2:
            if not users_with_values[callback.from_user.id]["hour_worked_trigger"]:
                users_with_values[callback.from_user.id]["hour_worked_trigger"] = True

            else:
                bot.delete_message(callback.message.chat.id, callback.message.message_id)
                for tmp_messages_id in users_with_values[callback.from_user.id]["date_message_id"]:
                    bot.delete_message(callback.message.chat.id, tmp_messages_id)
                users_with_values[callback.from_user.id]["date_message_id"] = []
                calendar_call(callback.from_user.id)

            date_id = bot.send_message(callback.message.chat.id, f"Вы выбрали дату: {callback.data}")
            users_with_values[callback.from_user.id]["date"] = callback.data
            hour_id = bot.send_message(callback.message.chat.id, "Введите количество отработанных часов:")
            users_with_values[callback.from_user.id]["date_message_id"].append(date_id.message_id)
            users_with_values[callback.from_user.id]["date_message_id"].append(hour_id.message_id)
            users_with_values[callback.from_user.id]["logical_hour_var"] = True


bot.infinity_polling()
