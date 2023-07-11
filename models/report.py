from typing import Dict
from datetime import datetime
from aiogram.types import Message, ReplyKeyboardRemove


class Report:
    """Класс Отчета"""

    def __init__(self, message: Message):
        self.message = message

        self.money = ...
        self.project = ...
        self.payment_method = ...
        self.department = ...
        self.comment = ...
        self.date = str(datetime.now().date())
        self.time = self.get_time()
        self.id = "".join(['@', str(self.message.from_user.username)])

    def from_dict(self, data: Dict):
        """Перевод из словаря в данные 'отчета' """
        self.money = data.get("money")
        self.project = str(data.get("project"))[1:]
        self.payment_method = str(data.get("payment_method"))[1:]
        self.department = data.get("departament")[1:]
        if data.get("comment") is not None:
            self.comment = data.get("comment")
        else:
            self.comment = None

    def to_dict(self):
        """Перевод из данных 'отчета' в словарь"""
        data = {
            "money": self.money,
            "project": self.project,
            "payment_method": self.payment_method,
            "department": self.department,
            "comment": self.comment,
            "date": self.date,
            "time": self.time,
            "id": self.id
        }
        return data

    async def print_info(self):
        """Вывод данных об отчете в сообщении"""
        if self.comment is None:
            await self.message.reply(f"Сумма расхода: {self.money} руб.\n"
                                     f"Проект: {self.project}\n"
                                     f"Способ оплаты: {self.payment_method}\n"
                                     f"Департамент: {self.department}\n\n"
                                     f"Дата составления отчета: {self.date}\n"
                                     f"Время составления отчета: {self.time}\n"
                                     f"id автора отчета: {self.id}", reply_markup=ReplyKeyboardRemove())
        else:
            await self.message.reply(f"Сумма расхода: {self.money} руб.\n"
                                     f"Проект: {self.project}\n"
                                     f"Способ оплаты: {self.payment_method}\n"
                                     f"Департамент: {self.department}\n"
                                     f"Комментарий: {self.comment}\n\n"
                                     f"Дата составления отчета: {self.date}\n"
                                     f"Время составления отчета: {self.time}\n"
                                     f"id автора отчета: {self.id}")

    def get_time(self):
        time = datetime.now().time()
        hours = str(time.hour)
        minutes = str(time.minute)
        second = str(time.second)
        formatted_time = ":".join([hours, minutes, second])
        return formatted_time
