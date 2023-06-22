
import telebot
import requests

# Telegram Bot API token
telegram_api_token = '6092366237:AAF9C5syqyMx2m8DNoJ9qJepymSWCDqd1MU'

# OpenWeatherMap API key
weather_api_key = '3947edb38e0696350a30dbfacc782bd5'

# Weather condition emojis
weather_emojis = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Thunderstorm': '⛈️',
    'Snow': '❄️',
    'Mist': '🌫️',
    'Smoke': '🌫️',
    'Haze': '🌫️',
    'Dust': '🌫️',
    'Fog': '🌫️',
}

bot = telebot.TeleBot(telegram_api_token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = telebot.types.KeyboardButton(text='Check weather')
    markup.add(button)

    bot.reply_to(message, "Welcome to the Weather Bot!\n\n"
                           "Tap the 'Check weather' button to get the weather forecast." +
                           "\nType /cancel to cancel.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Check weather')
def ask_weather_location(message):
    bot.reply_to(message, "Please enter a country or city name:")

@bot.message_handler(func=lambda message: True)
def send_weather_data(message):
    try:
        location = message.text

        # Get the weather data for the provided location
        weather_data = get_weather_data(location)

        if weather_data:
            # Get the emoji corresponding to the weather status
            weather_emoji = weather_emojis.get(weather_data['weather_status'], '')

            # Send the weather data as a reply to the user
            reply = f"{weather_emoji} Weather in {location}: {weather_data['weather_status']}\n\n" \
                    f"Temperature: {weather_data['temperature']} K\n\n" \
                    f"Humidity: {weather_data['humidity']} %\n\n" \
                    f"Wind Speed: {weather_data['wind_speed']} m/s\n\n" \
                    f"Longitude: {weather_data['longitude']}\n\n" \
                    f"Latitude: {weather_data['latitude']}\n\n" \
                    f"Feels Like: {weather_data['feels_like']} K\n\n" \
                    f"Pressure: {weather_data['pressure']} hPa"

            # Remove the custom keyboard and send the weather data
            bot.reply_to(message, reply, reply_markup=telebot.types.ReplyKeyboardRemove())

            # Ask the user if they want to check the weather again
            markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button = telebot.types.KeyboardButton(text='Check weather')
            markup.add(button)

            bot.reply_to(message, "Tap the 'Check weather' button to get the weather forecast.", reply_markup=markup)
        else:
            reply = "Sorry, I couldn't fetch the weather data for that location."
            bot.reply_to(message, reply)

    except IndexError:
        bot.reply_to(message, "Please provide a location name or tap the 'Check weather' button.")


def get_weather_data(location):
    try:
        # Make a request to the OpenWeatherMap API using the location name and API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}"
        response = requests.get(url)
        data = response.json()

        # Extract the required weather data from the JSON response
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        longitude = data['coord']['lon']
        latitude = data['coord']['lat']
        feels_like = data['main']['feels_like']
        pressure = data['main']['pressure']
        weather_status = data['weather'][0]['main']

        return {
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'longitude': longitude,
            'latitude': latitude,
            'feels_like': feels_like,
            'pressure': pressure,
            'weather_status': weather_status
        }
    except Exception as e:
        return None


bot.polling()
