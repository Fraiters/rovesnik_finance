import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from expenses.handlers.other_handler import OtherHandler
from expenses.handlers.report_handler import ReportHandler
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from general.general_handlers import GeneralHandler
from expenses.db.expenses_db import ExpensesDb


class TelegramBot:
    """Класс для запуска телеграм бота"""
    bot = Bot(token=os.getenv('TOKEN'))
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)
    db = ExpensesDb()

    async def on_startup(self, _):
        self.db.create_table_reports()

    def run(self):
        general_handler = GeneralHandler(bot=self.bot)
        report_handler = ReportHandler(bot=self.bot, db=self.db)
        other_handler = OtherHandler()

        general_handler.registration(dp=self.dp)
        report_handler.registration(dp=self.dp)
        other_handler.registration(dp=self.dp)

        executor.start_polling(dispatcher=self.dp, skip_updates=True, on_startup=self.on_startup)


if __name__ == '__main__':
    telegram_bot = TelegramBot()
    telegram_bot.run()
