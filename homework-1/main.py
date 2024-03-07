import csv
import psycopg2


def get_data_from_csv(file_path: str) -> list:
    """
    Get data from CSV-file to list.
    :param file_path: path to CSV-file.
    :return: list with data
    """
    data = []

    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)

        # Skip the title if there is one
        next(csv_reader)

        # Reading data from a CSV file and adding it to the list
        for row in csv_reader:
            data.append(row)

    return data


def append_data_to_sql(data: list, name_table: str) -> None:
    """
    Add data to SQL-table.
    :param data: list with data
    :param name_table: name of SQL-table
    :return: None
    """
    connection = psycopg2.connect(host=user_host, database='north', user=username, password=user_password)
    try:
        with connection:

            with connection.cursor() as cur:

                query = ("INSERT INTO " + name_table + " VALUES (") + '%s,' * len(data[0])
                query = query[:-1] + ")"

                for item in data:
                    cur.execute(query, tuple(item))

    finally:
        connection.close()
