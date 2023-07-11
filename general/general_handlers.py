from aiogram import Bot, Dispatcher
from aiogram.types import Message
from settings import GENERAL_BUTTONS
from general.general_keyboards import GeneralKb


class GeneralHandler:
    """Класс главных хендлеров"""

    def __init__(self, bot: Bot,):  # db: Db):
        self.bot = bot
        self.general_kb = GeneralKb()
        # self.fsm_admin = FsmReport()
        # self.db = db

    async def commands_start(self, message: Message):
        """Хендлер для команд 'start', 'help' """
        try:
            kb = self.general_kb.add(GENERAL_BUTTONS)
            await self.bot.send_message(message.from_user.id, 'Привет, на связи бот "Ровесник Финансы"',
                                        reply_markup=kb)
        except:
            await message.reply('Общение с ботом через лс, пожалуйста напишите ему: \n @rovesnik_finance_bot')

    def registration(self, dp: Dispatcher):
        """Регистрация главных хендлеров"""
        dp.register_message_handler(callback=self.commands_start, commands=['start', 'help'])
