import csv
import requests

SITC_INFO_URL = 'https://comtrade.un.org/Data/cache/classificationS2.json'
SITC_PATH = '../data/sitc2.csv'


def main():
    """Fetches SITC Standard codes from a given url and stores them as csv for ease of use later"""
    print('Fetching & converting SITC data...')
    res = requests.get(SITC_INFO_URL)
    res.raise_for_status()

    sitc_codes = res.json()['results']
    with open(SITC_PATH, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['id', 'text', 'parent'])
        writer.writeheader()
        writer.writerows(sitc_codes)

    print('Done!')


if __name__ == '__main__':
    main()