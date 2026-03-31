import sys
import functools
import sqlite3
import json
from datetime import datetime

def call_tracer(func=None, *, log_destination=sys.stdout):

    if func is None:
        return lambda func: call_tracer(func, log_destination=log_destination)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_data = {
                'timestamp': timestamp,
                'function_name': func.__name__,
                'parameters': {
                    'args': args,
                    'kwargs': kwargs
                },
                'outcome': result
            }

            if isinstance(log_destination, str) and log_destination.endswith('.json'):
                try:
                    with open(log_destination, 'r') as log_file:
                        try:
                            all_logs = json.load(log_file)
                        except json.JSONDecodeError:
                            all_logs = []
                except FileNotFoundError:
                    all_logs = []
                all_logs.append(log_data)
                with open(log_destination, 'w') as log_file:
                    json.dump(all_logs, log_file, indent=4)
            elif isinstance(log_destination, sqlite3.Connection):
                cursor = log_destination.cursor()
                cursor.execute('''INSERT INTO function_log(timestamp, function_name, parameters, outcome) 
                                  VALUES (?, ?, ?, ?)''',
                               (timestamp, func.__name__, str(args), str(result)))
                log_destination.commit()
            else:
                log_destination.write(f'{log_data}\n')

            return result

        except Exception as error:
            print(f"An error occurred in {func.__name__}: {error}")
            raise

    return wrapper

def setup_log_table(connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS function_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            function_name TEXT,
            parameters TEXT,
            outcome TEXT
        )
    ''')
    connection.commit()

def display_logs(connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM function_log')
    log_records = cursor.fetchall()
    for record in log_records:
        print(record)


#Примеры:
@call_tracer(log_destination=sys.stderr)  #Логирование в stderr
def increase(x):
    return x + 3


@call_tracer(log_destination='logger.json')  #Логирование в JSON-файл
def decrease(x):
    return x - 1


@call_tracer(log_destination='log_data.json')  #Логирование в JSON-файл
def f_2(x):
    return x ** 2


db_conn = sqlite3.connect(':memory:')
setup_log_table(db_conn)


@call_tracer(log_destination=db_conn)
def f_3(x):
    return x ** 3


cursor = db_conn.cursor()   #Добавление данных в базу данных
cursor.execute("INSERT INTO function_log (timestamp, function_name, parameters, outcome) VALUES ('2024-01-01', 'example', '2', '4')")
db_conn.commit()

increase(7)
decrease(9)
f_2(5)
f_3(4)

display_logs(db_conn)

db_conn.close()