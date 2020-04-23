import csv
from typing import Dict, List


def sort_by_similarity(matching_list: List[dict], descending: bool = True) -> List[dict]:
    return sorted(matching_list, key=lambda x: x['similarity'], reverse=descending)


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


def find_matching_intersections(oeance_candidates: Dict) -> List:
    """
    Returns a list of intersection from oenace_candidates of different approaches (currently using text_similarities
    and inverted_index)
    """
    all_matchings = []

    for method, matchings in oeance_candidates.items():
        all_matchings.append([(item['oenace_code'], item['oenace_title']) for item in matchings])

    return list(set.intersection(*map(set, all_matchings)))
