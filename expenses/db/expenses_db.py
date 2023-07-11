import sqlite3
from sqlite3 import Cursor
from sqlite3 import Connection
from typing import Dict

from expenses.db.settings_db import DB_REPORTS_COMMANDS


class ExpensesDb:
    """Класс работы с БД 'Расходы' """

    def __init__(self):
        self.connection = sqlite3.connect('expenses.db')  # type: Connection
        self.cursor = self.connection.cursor()  # type: Cursor

    def create_table_reports(self):
        """Создание таблицы отчетов в БД"""
        command = DB_REPORTS_COMMANDS.get("create_report_table")
        self.connection.execute(command)
        self.connection.commit()

    async def insert_record_report(self, data: Dict):
        """Добавление записи в таблицу отчетов"""
        command = DB_REPORTS_COMMANDS.get("insert_report")
        self.cursor.execute(command, tuple(data.values()))
        self.connection.commit()
