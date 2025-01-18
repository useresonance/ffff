from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext
import logging
import bcrypt

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Простая база данных для хранения пользователей и их данных
users_db = {}
bookings_db = {}

# Функция для регистрации
async def register(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id in users_db:
        await update.message.reply_text("Вы уже зарегистрированы.")
    else:
        await update.message.reply_text("Введите свой пароль для регистрации.")
        return "WAITING_FOR_PASSWORD"

# Функция для логина
async def login(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in users_db:
        await update.message.reply_text("Вы не зарегистрированы. Используйте команду /register для регистрации.")
    else:
        await update.message.reply_text("Введите ваш пароль для входа.")
        return "WAITING_FOR_LOGIN_PASSWORD"

# Обработка пароля для регистрации
async def handle_registration_password(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    password = update.message.text
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_db[chat_id] = {'password': hashed_password}
    await update.message.reply_text("Вы успешно зарегистрированы!")

# Обработка пароля для входа
async def handle_login_password(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    password = update.message.text
    if bcrypt.checkpw(password.encode('utf-8'), users_db[chat_id]['password']):
        await update.message.reply_text("Вы успешно вошли!")
    else:
        await update.message.reply_text("Неверный пароль. Попробуйте снова.")

# Функция для бронирования
async def book_table(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in users_db:
        await update.message.reply_text("Для бронирования стола необходимо зарегистрироваться. Используйте команду /register.")
        return
    
    await update.message.reply_text("Введите количество человек для бронирования.")
    return "WAITING_FOR_BOOKING"

# Обработка бронирования
async def handle_booking(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    num_people = update.message.text
    bookings_db[chat_id] = {'num_people': num_people}
    await update.message.reply_text(f"Ваш стол забронирован для {num_people} человек.")

# Функция для старта бота
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я помогу вам зарегистрироваться, войти и забронировать стол. http://127.0.0.1:5500/templates/\n"
                                    "Используйте команды:\n"
                                    "/register - регистрация\n"
                                    "/login - вход\n"
                                    "/book - бронирование стола.")

# Основная функция, которая запускает бота
def main():
    # Укажите ваш токен, полученный от BotFather
    TOKEN = "8184498313:AAEYbSjbu-qdgDGei81g9mVrilmB6CiFBRI"
    
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("book", book_table))

    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_registration_password))  # Изменено
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_login_password))        # Изменено
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_booking))                # Изменено

    application.run_polling()

if __name__ == '__main__':
    main()
