import csv
import psycopg2
import os


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


if __name__ == "__main__":
    # Add data from customers_data.csv to customers sql-table
    path_customers_data = os.path.join("north_data", "customers_data.csv")

    customers_data = get_data_from_csv(path_customers_data)

    append_data_to_sql(customers_data, 'customers')

    # Add data from employees_data.csv to employees sql-table
    path_employees_data = os.path.join("north_data", "employees_data.csv")

    employees_data = get_data_from_csv(path_employees_data)

    append_data_to_sql(employees_data, 'employees')

    # Add data from orders_data.csv to orders sql-table
    path_orders_data = os.path.join("north_data", "orders_data.csv")

    orders_data = get_data_from_csv(path_orders_data)

    append_data_to_sql(orders_data, 'orders')
