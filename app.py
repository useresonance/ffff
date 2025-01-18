from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешаем все источники

app = Flask(__name__)

# Замените на ваш API токен
TELEGRAM_BOT_TOKEN = '8184498313:AAEYbSjbu-qdgDGei81g9mVrilmB6CiFBRI'
CHAT_ID = '-4775708239'  # ID чата, куда будут отправляться уведомления

# Функция для отправки сообщений в Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    # Получаем данные из запроса
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    date = data['date']
    time = data['time']
    guests = data['guests']

    # Формируем сообщение для отправки в Telegram
    message = f"Новая бронь:\n\nИмя: {name}\nEmail: {email}\nТелефон: {phone}\nДата: {date}\nВремя: {time}\nКоличество гостей: {guests}"

    # Отправляем сообщение в Telegram
    send_to_telegram(message)

    # Отправляем успешный ответ
    return jsonify({"message": "Бронирование успешно!"})

if __name__ == '__main__':
    app.run(debug=True)
