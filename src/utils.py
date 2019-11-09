import csv
from typing import Dict


def load_csv(path_to_file: str) -> Dict:
    with open(path_to_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = {row['ID']: row['Title'] for row in csv_reader}
    return rows
