from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from expenses.keyboards.report_kb import ReportKb
from aiogram.types import ReplyKeyboardRemove
from settings import REPORT_BUTTONS
from models.report import Report
from expenses.db.expenses_db import ExpensesDb


class FsmReport(StatesGroup):
    """Класс машины состояний для отчетов"""
    money = State()
    project = State()
    payment_method = State()
    department = State()
    prepare_comment = State()
    comment = State()
    check_report = State()


class ReportHandler:
    """Класс хендлеров для отчетов """

    def __init__(self, bot: Bot, db: ExpensesDb):
        self.bot = bot
        self.report_kb = ReportKb()
        self.fsm_report = FsmReport()
        self.db = db
        self.report = ...

    async def expenses(self, message: Message):
        """Хендлер для команды 'Расходы' """
        kb = self.report_kb.add(REPORT_BUTTONS.get("add_report"))
        await self.bot.send_message(message.from_user.id, 'Чтобы добавить отчет нажмите на "Добавить отчет"',
                                    reply_markup=kb)

    async def add_report(self, message: Message):
        """Хендлер для команды 'Добавить отчет' (Вход в машину состояний)"""
        await self.fsm_report.money.set()
        await message.reply("Введите Сумму расхода (в рублях)", reply_markup=ReplyKeyboardRemove())

    async def cancel(self, message: Message, state: FSMContext):
        """Выход из машины состояний"""
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')

    async def load_money(self, message: Message, state: FSMContext):
        """Загрузка суммы расхода"""
        async with state.proxy() as data:
            data['money'] = float(message.text)
        await self.fsm_report.next()
        kb = self.report_kb.add(REPORT_BUTTONS.get("project"))
        await message.reply('Выберете проект', reply_markup=kb)

    async def load_project(self, message: Message, state: FSMContext):
        """Загрузка проекта"""
        async with state.proxy() as data:
            data['project'] = message.text
        await self.fsm_report.next()
        kb = self.report_kb.add(REPORT_BUTTONS.get("payment_method"))
        await message.reply('Выберете способ оплаты', reply_markup=kb)

    async def load_payment_method(self, message: Message, state: FSMContext):
        """Загрузка способа оплаты"""
        async with state.proxy() as data:
            data['payment_method'] = message.text
        await self.fsm_report.next()
        kb = self.report_kb.add(REPORT_BUTTONS.get("departament"))
        await message.reply('Выберете Департамент', reply_markup=kb)

    async def load_departament(self, message: Message, state: FSMContext):
        """Загрузка департамента"""
        async with state.proxy() as data:
            data['departament'] = message.text
        await self.fsm_report.next()
        kb = self.report_kb.add(REPORT_BUTTONS.get("comment"))
        await message.reply('Желаете добавить комментарий?', reply_markup=kb)

    async def prepare_comment(self, message: Message, state: FSMContext):
        """Подготовка к комментарию"""
        if message.text == "/Нет":
            async with state.proxy() as data:
                self.report = Report(message=message)
                self.report.from_dict(data=data)
                await self.report.print_info()

            await self.fsm_report.check_report.set()
            kb = self.report_kb.add(REPORT_BUTTONS.get("check_report"))
            await self.bot.send_message(message.from_user.id, "Все верно?", reply_markup=kb)

        elif message.text == "/Да":
            await self.fsm_report.next()
            await message.reply('Добавьте комментарий', reply_markup=ReplyKeyboardRemove())

    async def load_comment(self, message: Message, state: FSMContext):
        """Загрузка комментария"""
        async with state.proxy() as data:
            data['comment'] = message.text

        async with state.proxy() as data:
            self.report = Report(message=message)
            self.report.from_dict(data=data)
            await self.report.print_info()

        await self.fsm_report.check_report.set()
        kb = self.report_kb.add(REPORT_BUTTONS.get("check_report"))
        await self.bot.send_message(message.from_user.id, "Все верно?", reply_markup=kb)

    async def check_report(self, message: Message, state: FSMContext):
        """Проверка отчета"""
        if message.text == "/Нет,_необходима_правка":
            await self.fsm_report.money.set()
            await self.bot.send_message(message.from_user.id, "Введите Сумму расхода (в рублях)",
                                        reply_markup=ReplyKeyboardRemove())
        elif message.text == "/Да":
            data = self.report.to_dict()
            await self.db.insert_record_report(data=data)
            await self.bot.send_message(message.from_user.id, "Отчет составлен и сохранен",
                                        reply_markup=ReplyKeyboardRemove())
            await state.finish()

    def registration(self, dp: Dispatcher):
        """Регистрация хендлеров для отчетов"""
        dp.register_message_handler(callback=self.expenses, commands=['Расходы'])
        dp.register_message_handler(callback=self.add_report, commands=['Добавить_отчет'],
                                    state=None)
        dp.register_message_handler(callback=self.cancel, commands=['Отмена'],
                                    state='*')
        dp.register_message_handler(self.cancel, Text(equals='Отмена', ignore_case=True),
                                    state='*')
        dp.register_message_handler(callback=self.load_money,
                                    state=self.fsm_report.money)
        dp.register_message_handler(callback=self.load_project,
                                    state=self.fsm_report.project)
        dp.register_message_handler(callback=self.load_payment_method,
                                    state=self.fsm_report.payment_method)
        dp.register_message_handler(callback=self.load_departament,
                                    state=self.fsm_report.department)
        dp.register_message_handler(callback=self.prepare_comment,
                                    state=self.fsm_report.prepare_comment)
        dp.register_message_handler(callback=self.load_comment,
                                    state=self.fsm_report.comment)
        dp.register_message_handler(callback=self.check_report,
                                    state=self.fsm_report.check_report)
