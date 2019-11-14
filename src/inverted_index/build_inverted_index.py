import datetime
import csv

from pprint import pprint
from pathlib import Path

from inverted_index.preprocessing import pre_process
from inverted_index.utils import save_metadata


def build_inverted_index(docs: dict) -> dict:
    inverted_index = {}

    print('Started parsing categories: {}'.format(datetime.datetime.now()))

    i = 0
    for category_id, category_words in docs.items():
        words_counter = {}

        for word in category_words:
            if word not in words_counter:
                words_counter[word] = 0

            words_counter[word] += 1

        document_inverted_index = {
            k: (category_id, v) for k, v in words_counter.items()
        }

        for k, v in document_inverted_index.items():
            inverted_index.setdefault(k, []).append(v)

        i += 1

    print('Finished parsing categories: {}'.format(datetime.datetime.now()))

    print('\nInverted Index: ')
    pprint({k: sorted(v) for k, v in inverted_index.items()})

    return inverted_index


def parse_oeance_document(method: str = None) -> dict:
    """
    Parses documents and returns a dictionary representing documents and its corresponding words
    """
    docs = {}

    path = Path('../data/preprocessed/oenace2008.csv')

    with open(path) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')

        for i, line in enumerate(read_csv):

            # skip header line
            if i == 0:
                continue

            # Split line by fetching category id and category description
            category_id, category_description = line[1], line[3]

            # do the cleanup
            category_description = pre_process(category_description, method)

            docs[category_id] = category_description

        print('Finished parsing categories: {}'.format(datetime.datetime.now()))
    return docs


def main():
    method = 'lemmatizing'
    documents = parse_oeance_document(method)

    # build basic package inverted index
    inverted_index = build_inverted_index(documents)
    save_metadata(method=method, inverted_index=inverted_index, documents=documents)


if __name__ == '__main__':
    main()
