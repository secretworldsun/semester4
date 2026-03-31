import sqlite3
from datetime import datetime


class CurrencyRatesCRUD:
    def __init__(self, currency_rates_obj):
        self.__connection = sqlite3.connect('currency_rates.db')
        self.cursor = self.__connection.cursor()
        self.currency_rates = currency_rates_obj
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS currency_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                date TEXT NOT NULL
            )
        """)
        self.__connection.commit()

    def create(self, data=None):
        try:
            if data is None:
                raw_data = self.currency_rates.get_all_rates()
                data = [
                    {
                        'char_code': code,
                        'name': name,
                        'value': value,
                        'date': date
                    }
                    for code, name, value, date in raw_data
                ]

            if not data:
                print("Нет данных для записи")
                return False

            sql = """
                INSERT INTO currency_rates 
                (char_code, name, value, date)
                VALUES (:char_code, :name, :value, :date)
            """

            self.cursor.executemany(sql, data)
            self.__connection.commit()
            print(f"Успешно записано {len(data)} записей")
            return True

        except Exception as e:
            print(f"Ошибка при записи в базу данных: {e}")
            self.__connection.rollback()
            return False

    def read(self, char_code=None):
        try:
            if char_code:
                self.cursor.execute("""
                    SELECT char_code, name, value, date 
                    FROM currency_rates 
                    WHERE char_code = ?
                    ORDER BY date DESC
                """, (char_code,))
            else:
                self.cursor.execute("""
                    SELECT char_code, name, value, date 
                    FROM currency_rates 
                    ORDER BY date DESC
                """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при чтении из базы данных: {e}")
            return []

    def update_rates(self):
        try:
            if not self.currency_rates.update_rates():
                return False
            return self.create()
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
            return False

    def close(self):
        try:
            self.__connection.close()
        except sqlite3.Error as e:
            print(f"Ошибка при закрытии соединения: {e}")


class ViewController:
    def __init__(self, currency_rates):
        self.currency_rates = currency_rates

    def __call__(self):
        rates = self.currency_rates.get_all_rates()
        if not rates:
            return "Нет данных о курсах валют"
        
        result = ["Текущие курсы валют:"]
        for code, name, value, date in rates:
            result.append(f"{code} ({name}): {value} руб. (на {date})")
        
        return "\n".join(result)