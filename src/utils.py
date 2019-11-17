import csv
from typing import Dict


def load_csv(path_to_file: str) -> Dict:
    with open(path_to_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = {row['ID']: row['Title'] for row in csv_reader}
    return rows


def load_correspondence_tables(path_to_file: str, system: str) -> Dict:
    system = system.upper()
    with open(path_to_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = {row['SITC2']: row[system] for row in csv_reader}
    return rows


def load_enriched_sitc_codes(path_to_file: str) -> Dict:
    with open(path_to_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = {row['ID']: row["Mapping"].split('~') for row in csv_reader}
    return rows
