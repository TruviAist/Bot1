# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import json

# ?? Вставь сюда токен своего бота от BotFather
TOKEN = 'ТВОЙ_ТОКЕН_ЗДЕСЬ'
REACTION_EMOJI = '??'

# ?? Загрузка списка запрещённых слов
def load_bad_words():
    try:
        with open('bad_words.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# ? Проверка текста на наличие запрещённых слов
def contains_bad_words(text, bad_words):
    lowered = text.lower()
    for word in bad_words:
        if word.lower() in lowered:
            return True
    return False

# ?? Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.message.from_user
    chat_id = update.message.chat.id
    text = update.message.text or ""

    bad_words = load_bad_words()

    # Ставим эмодзи-реакцию
    try:
        await context.bot.send_reaction(chat_id=chat_id, message_id=update.message.message_id, emoji=REACTION_EMOJI)
    except Exception as e:
        print(f"Ошибка при установке реакции: {e}")

    # Проверяем на запрещённые слова
    if contains_bad_words(text, bad_words):
        try:
            await update.message.delete()
            await context.bot.ban_chat_member(chat_id=chat_id, user_id=user.id)
            print(f"Забанен {user.username} за: {text}")
        except Exception as e:
            print(f"Ошибка при удалении/бане: {e}")

# ?? Команда /id — присылает ID группы
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"ID группы: {chat_id}")

# ?? Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("id", get_chat_id))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
