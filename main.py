import telebot
import requests
import sys


weather_token = "994bb813145553757b5c55b37e7aa3e8"
api_token = '6038018331:AAGKJHoKhJytQ6QNMsorsET0qWh57DAPpWk'
bot = telebot.TeleBot(api_token)

def get_weather(city, token):
   emoji = {"Clear": "Clear \U00002600", "Clouds": "Clouds \U00002601", "Rain": "Rain \U00002614",\
            "Drizzle": "Drizzle \U00002614", "Thunderstorm": "Thunderstorm \U000026A1", "Snow": "Snow \U0001F328",\
            "Mist": "Mist \U0001F32B"}

   try:
        req = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric")
        data = req.json()

        city_d = data['name']
        cur_weather = data["main"]["temp"]
        weather = data["weather"][0]["main"]
        if weather in emoji:
            em = emoji[weather]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        return f'City: {city_d}\nTemrature: {cur_weather} C\nWeather: {em}\nHumidity: {humidity} %\nPressure: {pressure} mmHg'

   except Exception as e:
        print(e)
        print('Name error')

@bot.message_handler(commands=['stop'])
def stop():
    bot.stop_polling()

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.reply_to(message, 'Hi, I can tell you about the weather')
    bot.send_message(message.chat.id, 'Print your city in English or stop-command')
    bot.register_next_step_handler(msg, print_w)


def print_w(message):
    city = message.text
    msg = bot.reply_to(message, get_weather(city, weather_token))
    bot.send_message(message.chat.id, "Print your city in English or stop-command")
    bot.register_next_step_handler(msg, print_w)


bot.polling()


