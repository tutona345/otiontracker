
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler
import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

users_data = {}
signal_sources = ['OptionTracker (AI)', 'EliteSignals', 'TrendWatch']

# Обучение
education_blocks = [
    ("Бинарные опционы", "Это форма торговли, где трейдер прогнозирует рост или падение цены актива."),
    ("Свечи и паттерны", "Японские свечи показывают поведение цены. Паттерны помогают предсказать движение."),
    ("Таймфреймы", "Это временной интервал одной свечи. Например, 1m, 5m, 15m и т.д."),
    ("Психология", "Эмоции влияют на решения. Управляй страхом и жадностью."),
    ("Капитал", "Не рискуй больше 2% от депозита в одной сделке.")
]

# Главное меню
main_menu = ReplyKeyboardMarkup([
    [KeyboardButton("Получить сигнал"), KeyboardButton("Дать сигнал")],
    [KeyboardButton("График"), KeyboardButton("Обучение")],
    [KeyboardButton("Мой баланс"), KeyboardButton("Статистика")],
    [KeyboardButton("Изменить язык")]
], resize_keyboard=True)

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in users_data:
        keyboard = [
            [InlineKeyboardButton("Русский", callback_data='set_lang_ru')],
            [InlineKeyboardButton("English", callback_data='set_lang_en')]
        ]
        update.message.reply_text(
            "Выберите язык / Choose your language:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        lang = users_data[user_id]['lang']
        welcome = "Добро пожаловать обратно!" if lang == 'ru' else "Welcome back!"
        update.message.reply_text(welcome, reply_markup=main_menu)

def set_language(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    lang = 'ru' if 'ru' in query.data else 'en'
    users_data[user_id] = {'lang': lang, 'balance': 0, 'signals': [], 'vip': False}
    welcome = "Я Ваш помощник по торговле!" if lang == 'ru' else "I'm your trading assistant!"
    query.edit_message_text(welcome)
    context.bot.send_message(chat_id=user_id, text=welcome, reply_markup=main_menu)

def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    lang = users_data.get(user_id, {}).get('lang', 'ru')
    text = update.message.text.lower()

    if 'сигнал' in text and 'дать' in text:
        update.message.reply_text("Введите сигнал (пример: EUR/USD вверх через 5 минут)")
    elif 'сигнал' in text:
        signal = f"Сигнал от {signal_sources[0]}: EUR/USD Вверх (demo)"
        update.message.reply_text(signal)
    elif 'график' in text:
        update.message.reply_photo(photo='https://i.ibb.co/kcFYc6x/chart-sample.jpg', caption="График EUR/USD")
    elif 'обучение' in text:
        for title, content in education_blocks:
            update.message.reply_text(f"{title}:)
{content}")
    elif 'баланс' in text:
        bal = users_data[user_id]['balance']
        msg = f"Ваш баланс: {bal}$" if lang == 'ru' else f"Your balance: {bal}$"
        update.message.reply_text(msg)
    elif 'статист' in text:
        count = len(users_data[user_id]['signals'])
        msg = f"Вы отправили {count} сигналов." if lang == 'ru' else f"You've submitted {count} signals."
        update.message.reply_text(msg)
    elif 'язык' in text:
        start(update, context)
    else:
        users_data[user_id]['signals'].append((datetime.datetime.now(), text))
        msg = "Сигнал записан." if lang == 'ru' else "Signal recorded."
        update.message.reply_text(msg)

def main():
    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(set_language))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()
