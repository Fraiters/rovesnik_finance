# Команды БД для отчета
DB_REPORTS_COMMANDS = {
    "create_report_table": 'CREATE TABLE IF NOT EXISTS reports(money TEXT, project TEXT, payment_method TEXT, '
                           'departament TEXT, comment TEXT, date TEXT, time TEXT, id TEXT)',
    "insert_report": 'INSERT INTO  reports VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
    "select_all_reports": 'SELECT * FROM reports'
}
