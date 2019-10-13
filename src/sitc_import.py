import csv
import requests

SITC_INFO_URL = 'https://comtrade.un.org/Data/cache/classificationS2.json'
SITC_PATH = '../data/sitc2.csv'


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

    with open(SITC_PATH, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['ID', 'Title', 'Parent'])
        writer.writeheader()
        writer.writerows(sitc_codes)

    print('Done!')


if __name__ == '__main__':
    main()