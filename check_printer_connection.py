import subprocess
import time
from datetime import datetime
import telebot

API_CHAT_BOT = "6703403236:AAG6ce0KdDZIWyakRdxfCYmmoF_BnK9wVuY"
bot = telebot.TeleBot(API_CHAT_BOT)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    while True:
        def log_to_file(m):
            with open("ping_log.txt", "a") as log_file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"{timestamp} - {m}\n")

        printers = {"HP236": "192.168.223.64", "HP477": "192.168.223.155", "HP183": "192.168.223.26"}
        for key, value in printers.items():
            try:
                result = subprocess.run(["ping", value], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                        timeout=5)
                if result.returncode:
                    log_to_file(f"Connection lost to {value} ({key})")
                    bot.send_message(message.chat.id, f"Connection lost to {value} ({key})")

            except subprocess.TimeoutExpired:
                log_to_file(f"Timeout expired while pinging {value} ({key})")

        time.sleep(60)


bot.polling()
