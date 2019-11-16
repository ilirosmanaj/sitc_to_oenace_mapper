import csv
import requests

HS_URLs = {
    'HS1992': 'https://comtrade.un.org/data/cache/classificationH0.json',
    'HS1996': 'https://comtrade.un.org/data/cache/classificationH1.json',
    'HS2002': 'https://comtrade.un.org/data/cache/classificationH2.json',
    'HS2007': 'https://comtrade.un.org/data/cache/classificationH3.json',
    'HS2012': 'https://comtrade.un.org/data/cache/classificationH4.json',
    'HS2017': 'https://comtrade.un.org/data/cache/classificationH5.json'

}
HS_PATH_RAW = '../../data/raw/{file_name}.csv'


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
    """Fetches HS codes from a given url and stores them as csv for ease of use later"""
    print('Fetching & converting HS data...')

    for hs_system, hs_url in HS_URLs.items():
        print(f'Fetching {hs_system}...')
        res = requests.get(hs_url)
        res.raise_for_status()

        hs_codes = res.json()['results']
        hs_codes = [{
            'ID': code['id'],
            'Title': _format_description(code['text']),
            'Parent': code['parent']
        } for code in hs_codes]

        with open(HS_PATH_RAW.format(file_name=hs_system), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['ID', 'Title', 'Parent'])
            writer.writeheader()
            writer.writerows(hs_codes)

        print(f'Done writing {hs_system}.csv!', end='\n')


if __name__ == '__main__':
    main()
