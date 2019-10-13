import csv
from typing import List, Dict


def load_csv(path_to_file: str) -> List[Dict]:
    with open(path_to_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = [{'id': row['ID'], 'title': row['Title']} for row in csv_reader]
    return rows
