import json

import psycopg2

from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'

    params = config()

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> None:
    """
    Создает новую базу данных.
    :param params: параметры для подключения
    :param db_name: имя базы данных
    :return: None
    """
    conn = None
    try:
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {db_name}")
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
    finally:
        if conn is not None:
            conn.close()


def execute_sql_script(cur, script_file) -> None:
    """
    Выполняет скрипт из файла для заполнения БД данными.
    :param cur: курсор
    :param script_file: файл с SQL запросами
    :return: None
    """
    with open(script_file, 'r') as file:
        lines = file.readlines()

    clean_lines = [line for line in lines if not line.strip().startswith('--')]

    sql_commands = '\n'.join(clean_lines).split(';')

    for command in sql_commands:

        if command.strip():  # Проверяет, не является ли команда пустой
            cur.execute(command)


def create_suppliers_table(cur) -> None:
    """
    Создает таблицу suppliers.
    :param cur: курсор
    :return: None
    """
    cur.execute("""CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id serial NOT NULL,
    company_name varchar(100) NOT NULL,
    contact varchar(100) NOT NULL,
    address varchar(100) NOT NULL,
    phone varchar(30) NOT NULL,
    fax varchar(30) NOT NULL,
    homepage varchar(100) NOT NULL,
    products text NOT NULL
    )
    """)


def get_suppliers_data(json_file: str) -> list[dict]:
    """
    Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией.
    :param json_file: JSON-файл с данными
    :return: список со словарями
    """
    with open(json_file, 'r') as file:
        suppliers_data = json.load(file)
    return suppliers_data


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """
    Добавляет данные из suppliers в таблицу suppliers.
    :param cur: курсор
    :param suppliers: список со словарями
    :return: None
    """
    for j, supplier in enumerate(suppliers, start=1):
        for product in supplier['products']:
            cur.execute("INSERT INTO suppliers (supplier_id, company_name, contact, address, phone, fax, homepage, "
                        "products) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (j, supplier['company_name'], supplier['contact'], supplier['address'], supplier['phone'],
                         supplier['fax'], supplier['homepage'], product))


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    pass


if __name__ == '__main__':
    main()
