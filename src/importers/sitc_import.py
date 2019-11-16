import csv
import requests

SITC_INFO_URL = 'https://comtrade.un.org/Data/cache/classificationS2.json'
SITC_PATH_RAW = '../../data/raw/sitc2.csv'
SITC_PATH_PREPROCESSED = '../../data/preprocessed/sitc2.csv'


def _format_description(description: str) -> str:
    """
    Category description response from the API is created by 'CategoryID - Some Description'. We remove the 'ID -'
    from description to make it more suitable to perform text matching
    """
    try:
        return description.split('-')[1].strip()
    except IndexError:
        return description


def main():
    """Fetches SITC Standard codes from a given url and stores them as csv for ease of use later"""
    print('Fetching & converting SITC data...')
    res = requests.get(SITC_INFO_URL)
    res.raise_for_status()

    sitc_codes = res.json()['results']
    sitc_codes = [{
        'ID': code['id'],
        'Title': _format_description(code['text']),
        'Parent': code['parent']
    } for code in sitc_codes]

    valid_sitc_codes = []
    # fix titles for children and select only categories with code of length 4
    for sitc_code in sitc_codes:
        if '...' in sitc_code['Title']:
            parent_title = [row['Title'] for row in sitc_codes if row['ID'] == sitc_code['Parent'].split('.')[0]][0]
            sitc_code['Title'] = f"{parent_title} {sitc_code['Title'].replace('...', '')}"

        if len(sitc_code['ID']) == 4:
            valid_sitc_codes.append(sitc_code)

    with open(SITC_PATH_PREPROCESSED, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['ID', 'Title', 'Parent'])
        writer.writeheader()
        writer.writerows(valid_sitc_codes)

    print('Done!')


if __name__ == '__main__':
    main()