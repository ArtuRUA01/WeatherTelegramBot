import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = r'' # ENTER TOKEN
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['weather'])
def start_message(m):
    msg = bot.send_message(m.chat.id, 'Enter city')
    bot.register_next_step_handler(msg, weather_in_city)


def weather_in_city(m):

	try:
		city = m.text.capitalize()
		URL = f'https://www.meteoprog.ua/ua/weather/{city}/'
		
		r = requests.get(URL)
		soup = BeautifulSoup(r.text, "html.parser")

		dayoffWeek = soup.find('span', class_ = 'dayoffWeek').text.strip()
		dayoffMonth = soup.find('span', class_ = 'dayoffMonth').text.strip()
		min_t = soup.find('span', class_ = 'from').text.strip()
		max_t = soup.find('span', class_ = 'to').text.strip()
		description = soup.find('div',class_ = "infoPrognosis widthProg").text.strip()

		bot.send_message(m.chat.id ,
			f'\n{dayoffWeek} ({dayoffMonth})\n{description}\nМін.: {min_t}\nМакс.: {max_t}\nБільш детальніше можна дізнатись на сайті: {URL}\n')
	except Exception as e:
		bot.send_message(m.chat.id, 'Can`t find this city (maybe write this city without - or space)')

bot.polling()


