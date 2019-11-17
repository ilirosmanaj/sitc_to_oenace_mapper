import csv
from utils import load_csv, load_correspondence_tables

HARMONIZED_SYSTEM_NAMES = ['HS1992', 'HS1996', 'HS2002', 'HS2007', 'HS2012', 'HS2017']
SITC2_FILE_PATH = '../../data/preprocessed/sitc2.csv'
HS_FILE_PATH_RAW = '../../data/raw/{hs_system}.csv'
CORRESPONDENCE_FILE_PATH_PREPROCESSED = '../../data/correspondence_tables/preprocessed/{hs_system}toSITC2.csv'
ENRICHED_SITC_CODES_FILE_PATH = '../../data/correspondence_tables/mapped/enriched.csv'


def main():
    """Goes through all the correspondance files, and foreach of our sitc codes, fetches the descriptions used by the
    harmonized systems. These extra descriptions will later be used to better match based on text similarity"""
    sitc_codes = load_csv(SITC2_FILE_PATH)

    # load all harmonized system categories
    hs_codes = {hs: {} for hs in HARMONIZED_SYSTEM_NAMES}

    for hs_system in HARMONIZED_SYSTEM_NAMES:
        hs = load_csv(HS_FILE_PATH_RAW.format(hs_system=hs_system))
        hs_codes[hs_system] = hs

    # load all correspondence tables
    hs_correspondence_tables = {hs: {} for hs in HARMONIZED_SYSTEM_NAMES}

    for hs_system in HARMONIZED_SYSTEM_NAMES:
        hs = load_correspondence_tables(CORRESPONDENCE_FILE_PATH_PREPROCESSED.format(hs_system=hs_system), system=hs_system)
        hs_correspondence_tables[hs_system] = hs

    sitc_codes_enriched = {code: set() for code in sitc_codes.keys()}
    # foreach sitc_code, find its correspondent from hs_codes and store them as set
    for sitc_code in sitc_codes.keys():
        # go through all mappings and fetch its description
        for hs_system, mappings in hs_correspondence_tables.items():
            mapping = mappings.get(sitc_code)

            if mapping:
                # might need to change to get
                sitc_codes_enriched[sitc_code].add(hs_codes[hs_system][mapping])
    print(f'in total {len(sitc_codes_enriched)} and only {len([c for c, v in sitc_codes_enriched.items() if v])} '
          f'extended')

    # store the mapped stuff
    with open(ENRICHED_SITC_CODES_FILE_PATH, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Mapping'])
        for sitc_code, desc in sitc_codes_enriched.items():
            if desc:
                writer.writerow([sitc_code, '~'.join(desc)])

    print(f'Extended mapping stored under {ENRICHED_SITC_CODES_FILE_PATH}')


if __name__ == '__main__':
    main()
