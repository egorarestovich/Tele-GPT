import telebot
from g4f import *
from g4f.client import Client
import tokenandmore

client = Client()

TOKEN = tokenandmore.TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def main(message):
    full_name = f"{message.from_user.first_name} {message.from_user.last_name}" if message.from_user.last_name else message.from_user.first_name
    bot.send_message(message.chat.id, f"{full_name}, Привет👋, я ChatGPT, и готов ответить на все ваши вопросы! Просто нажми на меню, и выбери отправить запрос!\nЕсли будут ошибки, не ругайте меня, я только учусь😣")

def escape_markdown(text):
    """Экранирует специальные символы Markdown."""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!', '?']
    for char in special_chars:
        text = text.replace(char, '\\' + char)
    return text

@bot.message_handler(commands=['zapros'])
def zapros(message):
    bot.send_message(message.chat.id, "Введите ваш запрос:")
    @bot.message_handler()
    def tochatgpt(message):
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": message.text.lower()}],
                model="gpt-4o"
            )

            # Проверяем наличие ответов в choices
            if hasattr(response, 'choices') and len(response.choices) > 0:
                reply_text = response.choices[0].message.content
                if reply_text == 'Generated by BLACKBOX.AI, try unlimited chat https://www.blackbox.ai':
                    while reply_text != 'Generated by BLACKBOX.AI, try unlimited chat https://www.blackbox.ai':
                        response = client.chat.completions.create(
                            messages=[{"role": "user", "content": message.text.lower()}],
                            model="gpt-4o"
                        )
                        reply_text = response.choices[0].message.content
                # Экранируем специальные символы Markdown
                reply_text = escape_markdown(reply_text)

                # Отладочное сообщение для проверки текста перед отправкой
                print(f"Отправляемый текст: {reply_text}")


                # Отправляем сообщение в Telegram с использованием parse_mode 'MarkdownV2'
                bot.send_message(message.chat.id, reply_text, parse_mode='MarkdownV2')
            else:
                bot.send_message(message.chat.id, "Извините, я не смог получить ответ.")
                print("Ответ не содержит 'choices'.")  # Отладочное сообщение
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего запроса.")
            print(f"Ошибка: {e}")  # Логируем ошибку в консоль

bot.infinity_polling()