import csv


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
