from pprint import pprint
import click
from typing import List
from fuzzywuzzy import fuzz

from inverted_index.querying import perform_exploration
from src.utils import load_csv, load_enriched_sitc_codes
from inverted_index.utils import load_metadata

OENACE_FILE_PATH = '../data/preprocessed/oenace2008.csv'
SITC2_FILE_PATH = '../data/preprocessed/sitc2.csv'
SITC2_ENRICHED_FILE_PATH = '../data/correspondence_tables/mapped/enriched.csv'

TEXT_SIMILARITY_THRESHOLD = 65


def text_similarites(text1: str, text2: str, verbose: bool = False) -> int:
    # TODO: add more explanations of what this does from. Use https://github.com/seatgeek/fuzzywuzzy
    val = fuzz.token_set_ratio(text1, text2)
    if verbose:
        print(f'Similiartiy between {text1} and {text2} is: {val}')
    return val


def sort_by_similarity(matching_list: List[dict]) -> List[dict]:
    return sorted(matching_list, key=lambda x: x['similarity'], reverse=True)


@click.command()
@click.option('-e', '--use_enriched_sitc', required=True, is_flag=True, default=True)
def main(use_enriched_sitc: bool):
    oenace_codes = load_csv(OENACE_FILE_PATH)
    sitc_codes = load_csv(SITC2_FILE_PATH)
    sitc_enriched_codes = load_enriched_sitc_codes(SITC2_ENRICHED_FILE_PATH)

    method = 'lemmatizing'
    metadata = load_metadata(method)

    counter = 0
    total = 0
    for sitc_code, sitc_title in sitc_codes.items():
        total += 1

        if total > 20:
            pass
        # print(f"Findind a mapping for: '{sitc_title}'")

        if use_enriched_sitc:
            extending = sitc_enriched_codes.get(sitc_code, [])
            if extending: pass
                # print(f'Extending "{sitc_title}" with: {extending}')
            sitc_title_extendend = ".".join([sitc_title] + sitc_enriched_codes.get(sitc_code, []))
        else:
            sitc_title_extendend = sitc_title

        # hold a list of possible mapping candidates from oenace codes
        oenace_candidates = {
            'text_similarity': [],
            'inverted_index': [],
        }

        # step1: try to do exact name matching
        for oenace_code, oenace_title in oenace_codes.items():
            text_similarity = text_similarites(sitc_title_extendend, oenace_title)

            if text_similarity > TEXT_SIMILARITY_THRESHOLD:
                oenace_candidates['text_similarity'].append({
                    'oenace_code': oenace_code,
                    'oenace_title': oenace_title,
                    'similarity': text_similarity,
                })
        # sort by similiarty desc
        if oenace_candidates['text_similarity']:
            oenace_candidates['text_similarity'] = sort_by_similarity(oenace_candidates['text_similarity'])

        # step2: perform search using tf-idf weighting
        tf_idf_results = perform_exploration(query=sitc_title_extendend, method=method, metadata=metadata)
        if tf_idf_results:
            oenace_candidates['inverted_index'].extend([{
                'oenace_code': item[0],
                'oenace_title': oenace_codes[item[0]],
                'similarity': item[1],
            } for item in tf_idf_results])

        # step 4: a model
        # pprint(oenace_candidates)
        # find intersections from all steps
        all_matchings = []
        for method, matchings in oenace_candidates.items():
            all_matchings.append([(item['oenace_code'], item['oenace_title']) for item in matchings])

        intersections = set.intersection(*map(set, all_matchings))
        if intersections:
            counter += 1
            print(f"Findind a mapping for: '{sitc_title}'")
            for val in intersections:
                print(f' - {val}')
            print(end='\n\n')
        else:
            pass
            # print('Nothing found')
        # print(end='\n\n')

    print(f'Found a total of {counter} mappings from {total}')


if __name__ == '__main__':
    main()
