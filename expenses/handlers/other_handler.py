from aiogram import Dispatcher
from aiogram.types import Message
import json
import string


class OtherHandler:
    """Класс общих хендлеров"""
    async def all_send(self, message: Message):
        """Обработчик всех приходящих сообщений"""
        await self.censure(message=message)

    async def censure(self, message: Message):
        """Фильтр нецензурной брани"""
        censure_json_path = r'censure/static/censure.json'
        # множество слов отправленных в группу
        sent_words = {word.lower().translate(str.maketrans('', '', string.punctuation)) for word in
                      message.text.split(' ')}
        # множество нецензурных слов
        dirty_words = set(json.load(open(censure_json_path)))
        # проверка пересечения элементов множества
        if sent_words.intersection(dirty_words) != set():
            await message.reply('Нецензурная брань запрещена!')
            await message.delete()

    def registration(self, dp: Dispatcher):
        """Регистрация общих хендлеров"""
        dp.register_message_handler(callback=self.all_send)
