import csv

PATH_TO_RAW = '../data/raw/oenace2008.csv'
PATH_TO_PREPROCESSED = '../data/preprocessed/oenace2008.csv'


def main():
    """
    Filters out some records from the OENACE file, by selecting only products with
    four digits in the code (marked as level 4). The clean oeance file should endup with only 615 rows.
    """
    preprocessed = []
    with open(PATH_TO_RAW, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        preprocessed = [row for row in csv_reader if row['Level'] == '4']

    with open(PATH_TO_PREPROCESSED, 'w') as f:
        w = csv.DictWriter(f, preprocessed[0].keys())
        w.writeheader()
        w.writerows(preprocessed)


if __name__ == '__main__':
    main()
