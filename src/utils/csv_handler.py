import csv
import os


class CSVHandler:
    def __init__(self, path):
        self.path = path

    def file_is_exists(self):
        return os.path.exists(self.path)

    def create_csv(self, header: list):
        with open(self.path, 'w', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=';', lineterminator='\r')
            csv_writer.writerow(header)

    def update_rows(self, data: list):
        with open(self.path, 'a', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=';', lineterminator='\r')
            csv_writer.writerow(data)

    def read_column(self, column_name: str):
        values = []
        with open(self.path, encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                values.append(row[column_name])
        return values

    def remove_row_by_column_value(
        self, column_name: str, value_to_remove: str
    ):
        with open(self.path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            header = csv_reader.fieldnames
            updated_rows = [
                row
                for row in csv_reader
                if str(row[column_name]) != value_to_remove
            ]

        with open(self.path, 'w', encoding='utf-8') as file:
            if header:
                csv_writer = csv.DictWriter(
                    file, fieldnames=header, delimiter=';', lineterminator='\r'
                )
                csv_writer.writeheader()
                csv_writer.writerows(updated_rows)
