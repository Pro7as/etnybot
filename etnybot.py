import telebot
import requests
from datetime import datetime

url = "https://blockexplorer.bloxberg.org/api/api"


def get_token_balance(contract_address, address):
    querystring = {
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": contract_address,
        "address": address
    }

    response = requests.get(url, params=querystring)

    if response.status_code == 200:
        data = response.json()
        balance = int(data["result"]) / (10 ** 18)  # переводим баланс в единицы токена
        return balance
    else:
        return None


# Токен Etny и адреса нод
etny_contract_address = "0x549a6e06bb2084100148d50f51cf77a3436c3ae7"
android_node_address = "0x96FA971C5524b434d60c40f829633895C099d031"
liverpool_node_address = "0x3f01d724611f009133640BEbB7Fbc82fABeeda5E"
Vova_node_address = "0xb82B4A2c7E375116173921bCCDcD6990ac13ABBB"

# Создание бота и кнопок


bot = telebot.TeleBot("6265956103:AAGurOX3j_AyL9oMopBbfBl76bfNRh04BFE")

itembtn = telebot.types.KeyboardButton('Последние транзакции')
android_button = telebot.types.KeyboardButton('Android Node Balance')
Vova_button = telebot.types.KeyboardButton('Vova Node Balance')
liverpool_button = telebot.types.KeyboardButton('Liverpool Node Balance')

markup = telebot.types.ReplyKeyboardMarkup()
markup.add(Vova_button, android_button, liverpool_button, itembtn)


# Обработка нажатий на кнопки
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Etny статистика", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Android Node Balance")
def android_balance_handler(message):
    balance = get_token_balance(etny_contract_address, android_node_address)
    if balance:
        bot.reply_to(message, f"Android Node Balance: {balance}")
    else:
        bot.reply_to(message, "Error: unable to retrieve token balance.")


@bot.message_handler(func=lambda message: message.text == "Vova Node Balance")
def Vova_balance_handler(message):
    balance = get_token_balance(etny_contract_address, Vova_node_address)
    if balance:
        bot.reply_to(message, f"Vova Node Balance: {balance}")
    else:
        bot.reply_to(message, "Error: unable to retrieve token balance.")


@bot.message_handler(func=lambda message: message.text == "Liverpool Node Balance")
def liverpool_balance_handler(message):
    balance = get_token_balance(etny_contract_address, liverpool_node_address)
    if balance:
        bot.reply_to(message, f"liverpool Node Balance: {balance}")
    else:
        bot.reply_to(message, "Error: unable to retrieve token balance.")


@bot.message_handler(func=lambda message: message.text == "Последние транзакции")
def send_last_transactions(message):
    url = "https://blockexplorer.bloxberg.org/api/api"
    addresses = ["0xfeA7B9a2F18D6c8ECB67d3bF3F6700E62c3d0780", "0x023fd6FA8B1af56398A6418145Ba4E07513da02C",
                 "0x49bd1Cd00C0fFC78961C016d95CB56AeA03D3965"]
    for address in addresses:
        querystring = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "sort": "desc"
        }
        response = requests.get(url, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if data["result"]:
                tx_hash = data["result"][0]["hash"]
                timestamp = int(data["result"][0]["timeStamp"])
                dt_object = datetime.fromtimestamp(timestamp)
                message_text = f"Адрес {address}: последняя транзакция в {dt_object}"
                bot.send_message(message.chat.id, message_text)
            else:
                message_text = f"Адрес {address}: нет транзакций"
                bot.send_message(message.chat.id, message_text)
        else:
            message_text = f"Ошибка при получении транзакций для адреса {address}"
            bot.send_message(message.chat.id, message_text)


bot.polling()
