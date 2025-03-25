import logging
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "8028085053:AAHcrxENfsIp1t-GUgkgE-KLKPFDP8upCT0"  # Замените на свой токен

# Логирование
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


# Функция обработки команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Отправь /add <ссылка>, чтобы добавить её в мониторинг.")


# Функция обработки команды /add
async def add_url(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("⚠️ Пожалуйста, укажи ссылку: /add <url>")
        return

    url = context.args[0]
    command = f"python -m ebAlert.main links --add_url {url}"

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            await update.message.reply_text(f"✅ Ссылка добавлена: {url}")
        else:
            await update.message.reply_text(f"❌ Ошибка: {result.stderr}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")


# Функция обработки неизвестных сообщений
async def unknown(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("❓ Неизвестная команда. Используй /add <url>")


# Основная функция запуска бота
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_url))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    print("✅ Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_url))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    print("✅ Бот запущен!")
    app.run_polling(drop_pending_updates=True)  # <--- ЭТО ГЛАВНОЕ ИЗМЕНЕНИЕ
