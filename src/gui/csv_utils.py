import csv
from datetime import datetime

PATH_TO_MAPPING = '../data/mapping_results'


class CSVHandler:
    def __init__(self):
        self.path_to_results = PATH_TO_MAPPING
        self.column_names = ['SITC_CODE', 'OENACE_CODE']

    def store_results(self, mapping_results: dict, file_name: str):
        full_path = f'{self.path_to_results}/{file_name}.csv'

        with open(full_path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.column_names)
            writer.writeheader()

            for sitc_code, oenace_code in mapping_results.items():
                writer.writerow({'SITC_CODE': sitc_code, 'OENACE_CODE': oenace_code})
        return full_path

    def load_results(self, file_name) -> dict:
        mapping = {}
        with open(file_name, 'r') as csvfile:
            csvreader = csv.reader(csvfile, )

            # skip header
            next(csvreader)

            for row in csvreader:
                mapping[row[0]] = row[1]

        return mapping
