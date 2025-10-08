from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

GENRE, MOOD, DURATION, RESULT = range(4)

movies_db = [
    {"title": "Крестный отец", "genre": "криминал", "mood": "напряжённый", "duration": "длинный"},
    {"title": "Побег из Шоушенка", "genre": "драма", "mood": "добрый", "duration": "длинный"},
    {"title": "Темный рыцарь", "genre": "боевик", "mood": "экшн", "duration": "длинный"},
    {"title": "Форрест Гамп", "genre": "драма", "mood": "добрый", "duration": "длинный"},
    {"title": "Начало", "genre": "фантастика", "mood": "психологический", "duration": "длинный"},
    {"title": "Матрица", "genre": "фантастика", "mood": "экшн", "duration": "средний"},
    {"title": "Джанго освобожденный", "genre": "боевик", "mood": "экшн", "duration": "длинный"},
    {"title": "Бойцовский клуб", "genre": "драма", "mood": "психологический", "duration": "длинный"},
    {"title": "Зеленая книга", "genre": "драма", "mood": "добрый", "duration": "средний"},
    {"title": "Достать ножи", "genre": "триллер", "mood": "психологический", "duration": "средний"},
    {"title": "Однажды в Голливуде", "genre": "драма", "mood": "романтический", "duration": "длинный"},
    {"title": "Джокер", "genre": "драма", "mood": "психологический", "duration": "средний"},
    {"title": "Паразиты", "genre": "триллер", "mood": "напряжённый", "duration": "средний"},
    {"title": "Гравитация", "genre": "фантастика", "mood": "напряжённый", "duration": "короткий"},
    {"title": "Мальчишник в Вегасе", "genre": "комедия", "mood": "весёлый", "duration": "средний"},
    {"title": "Интерстеллар", "genre": "фантастика", "mood": "психологический", "duration": "длинный"},
    {"title": "Волк с Уолл-стрит", "genre": "комедия", "mood": "весёлый", "duration": "длинный"},
    {"title": "Остров проклятых", "genre": "триллер", "mood": "напряжённый", "duration": "длинный"},
    {"title": "Гладиатор", "genre": "боевик", "mood": "экшн", "duration": "длинный"},
    {"title": "Титаник", "genre": "драма", "mood": "романтический", "duration": "длинный"},
    {"title": "Криминальное чтиво", "genre": "криминал", "mood": "напряжённый", "duration": "длинный"},
    {"title": "Одержимость", "genre": "драма", "mood": "психологический", "duration": "средний"},
    {"title": "Дедпул", "genre": "комедия", "mood": "весёлый", "duration": "средний"},
    {"title": "Безумный Макс", "genre": "боевик", "mood": "экшн", "duration": "средний"},
    {"title": "Оно", "genre": "триллер", "mood": "напряжённый", "duration": "длинный"}
]
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает разговор и спрашивает о жанре."""
    user = update.effective_user

    reply_keyboard = [["боевик", "драма", "комедия"],
                      ["фантастика", "криминал", "триллер"]]

    await update.message.reply_text(
        f'Привет, {user.first_name}! Я подберу фильм по твоим предпочтениям ❤️\n\n'
        "Выбери один из основных жанров в меню:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбери жанр"
        ),
    )

    return GENRE


async def genre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает выбор жанра."""
    reply_keyboard = [["боевик", "драма", "комедия"],
                      ["фантастика", "криминал", "триллер"]]
    if update.message.text not in ["боевик", "драма", "комедия", "фантастика", "криминал", "триллер"]:
        await update.message.reply_text(
            "Такого жанра нет 🙃\n"
            "Пожалуйста, выбери один из предложенных вариантов в меню!",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбери жанр"
            ),
        )
        return GENRE

    context.user_data["genre"] = update.message.text
    reply_keyboard = [["романтический", "экшн", "добрый"],
                      ["напряжённый", "весёлый", "психологический"]]

    await update.message.reply_text(
        "Отлично! Теперь выбери настроение 😜",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбери настроение"
        ),
    )
    return MOOD


async def mood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает выбор настроения."""
    reply_keyboard = [["романтический", "экшн", "добрый"],
                      ["напряжённый", "весёлый", "психологический"]]
    if update.message.text not in ["романтический", "экшн", "добрый", "напряжённый", "весёлый", "психологический"]:
        await update.message.reply_text(
            "Такого настроения я не знаю 🙃\n"
            "Пожалуйста, выбери один из предложенных вариантов в меню!",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True
            )
        )
        return MOOD

    context.user_data["mood"] = update.message.text
    reply_keyboard = [["короткий", "средний", "длинный", "любой"]]

    await update.message.reply_text(
        "Хорошо! Последний вопрос: сколько времени у тебя есть? 🚀",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбери длительность"
        ),
    )
    return DURATION


async def duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает выбор длительности и показывает результат."""
    reply_keyboard = [["короткий", "средний", "длинный", "любой"]]
    if update.message.text not in ["короткий", "средний", "длинный", "любой"]:
        await update.message.reply_text(
            "Такого времени нет 🙃\n"
            "Пожалуйста, выбери один из предложенных вариантов в меню!",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True
            )
        )
        return DURATION

    # итог препдочтения
    genre_pref = context.user_data.get("genre", "")
    mood_pref = context.user_data.get("mood", "")
    duration_pref = context.user_data.get("duration", "любой")

    # цикл для подбора фильма
    suitable_movies = []
    for movie in movies_db:
        genre_match = not genre_pref or genre_pref in movie["genre"]
        mood_match = not mood_pref or mood_pref in movie["mood"]
        duration_match = (duration_pref == "любой") or (duration_pref in movie["duration"])

        if genre_match and mood_match and duration_match:
            suitable_movies.append(movie["title"])

    # Если ничего не найдено, показываем случайный фильм
    if not suitable_movies:
        import random
        suitable_movies = [random.choice(movies_db)["title"]]

    # Ограничение
    movies_to_show = suitable_movies[:3]
    movies_text = "\n- ".join(movies_to_show)

    await update.message.reply_text(
        f"Вот что я нашел для тебя:\n- {movies_text}\n\n"
        f"Приятного просмотра! 🎬\n\n"
        f"Если хочешь попробовать еще раз, нажми /start",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет и завершает разговор."""
    await update.message.reply_text(
        "Поиск отменен. Если захочешь попробовать снова, нажми /start",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

async def handle_unexpected_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает любые непредусмотренные сообщения."""
    await update.message.reply_text(
        "К сожалению, не понимаю, что ты говоришь(\n"
        "Нажми /start чтобы начать диалог."
    )


def main() -> None:
    """Запускает бота."""
    application = Application.builder().token("7967156469:AAGztoyX42NhQ8suQcZBFSB0g_c26fIN_e0").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GENRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, genre)],
            MOOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, mood)],
            DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, duration)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(filters.ALL, handle_unexpected_message)  # Обработка любых других сообщений
        ],
    )

    application.add_handler(conv_handler)

    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_unexpected_message))

    application.run_polling()


if __name__ == "__main__":
    main()