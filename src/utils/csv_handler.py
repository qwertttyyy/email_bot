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

    def read_row(self, row_name: str):
        values = []
        with open(self.path, encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                values.append(row[row_name])
        return values
