import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Введите ваш токен бота
TELEGRAM_TOKEN = '6417609698:AAG7Ry7gJlYbWN7U0RZFVsiPbyajhLQgY4k'
FLASK_API_URL = 'http://127.0.0.1:5000/weather/json/'  # Адрес вашего Flask API
# FLASK_API_URL = 'http://metar-service-production-e57b.up.railway.app:8080/weather/json/'

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Проверяем, указан ли код аэропорта
    if len(context.args) != 1:
        await update.message.reply_text('Пожалуйста, укажите код аэропорта, например: /weather uuee')
        return

    airport_code = context.args[0].upper()
    
    try:
        # Запрашиваем данные погоды через Flask API
        response = requests.get(f"{FLASK_API_URL}{airport_code}")
        response.raise_for_status()
        data = response.json()

        # Форматируем вывод для бота
        metar = data.get("metar", "Нет данных METAR")
        taf = data.get("taf", "Нет данных TAF")
        message = (
            f"**Аэропорт:** {data['name']} ({data['icao']})\n\n"
            f"**METAR:**\n{metar}\n\n"
            f"**TAF:**\n{taf}"
        )

        # Отправляем сообщение с погодой
        await update.message.reply_text(message, parse_mode="Markdown")

    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Ошибка при запросе данных: {e}")
    except KeyError:
        await update.message.reply_text("Не удалось получить данные для указанного аэропорта.")

# Основная функция запуска бота
def main():
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработка команды /weather
    application.add_handler(CommandHandler("weather", get_weather))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()