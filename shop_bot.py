from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN=os.getenv("8040763103:AAE8JDIsPUw6Lo0g7oU56oSyus9XWnabP8g")
ADMIN_ID = 123456789  # ВСТАВЬ СЮДА СВОЙ TELEGRAM ID

# Главное меню
main_keyboard = ReplyKeyboardMarkup(
    [
        ["🛍 Каталог", "📞 Контакты"],
        ["🛠 Техподдержка"]
    ],
    resize_keyboard=True
)

# Меню каталога
catalog_keyboard = ReplyKeyboardMarkup(
    [
        ["🔥 Товар 1 - 10$"],
        ["💎 Товар 2 - 20$"],
        ["⬅️ Назад"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в магазин 😎",
        reply_markup=main_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text == "🛍 Каталог":
        await update.message.reply_text(
            "Выберите товар:",
            reply_markup=catalog_keyboard
        )

    elif text in ["🔥 Товар 1 - 10$", "💎 Товар 2 - 20$"]:
        await update.message.reply_text(
            "✅ Заказ принят! Администратор свяжется с вами.",
            reply_markup=main_keyboard
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🛒 Новый заказ!\nОт: @{user.username}\nID: {user.id}\nТовар: {text}"
        )

    elif text == "📞 Контакты":
        await update.message.reply_text(
            "📱 Связь: @your_username",
            reply_markup=main_keyboard
        )

    elif text == "🛠 Техподдержка":
        await update.message.reply_text(
            "Напишите ваш вопрос, и мы передадим его администратору."
        )
        context.user_data["support"] = True

    elif text == "⬅️ Назад":
        await update.message.reply_text(
            "Главное меню:",
            reply_markup=main_keyboard
        )

    elif context.user_data.get("support"):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🛠 Сообщение в поддержку\nОт: @{user.username}\nID: {user.id}\nСообщение: {text}"
        )
        await update.message.reply_text(
            "✅ Ваше сообщение отправлено.",
            reply_markup=main_keyboard
        )
        context.user_data["support"] = False

    else:
        await update.message.reply_text(
            "Выберите кнопку из меню 👇",
            reply_markup=main_keyboard
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🔥 SHOP BOT PRO запущен...")
app.run_polling()
