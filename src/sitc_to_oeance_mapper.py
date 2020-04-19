import click
from typing import List
from fuzzywuzzy import fuzz

from gui.gui import start_gui
from inverted_index.querying import perform_exploration
from src.utils import load_csv, load_enriched_sitc_codes, find_matching_intersections
from inverted_index.utils import load_metadata

OENACE_FILE_PATH = '../data/preprocessed/oenace2008.csv'
SITC2_FILE_PATH = '../data/preprocessed/sitc2.csv'
SITC2_ENRICHED_FILE_PATH = '../data/correspondence_tables/mapped/enriched.csv'

TEXT_SIMILARITY_THRESHOLD = 75


def text_similarites(text1: str, text2: str, verbose: bool = False) -> int:
    # TODO: add more explanations of what this does from. Use https://github.com/seatgeek/fuzzywuzzy
    val = fuzz.token_set_ratio(text1, text2)
    if verbose:
        print(f'Similiartiy between {text1} and {text2} is: {val}')
    return val


def sort_by_similarity(matching_list: List[dict]) -> List[dict]:
    return sorted(matching_list, key=lambda x: x['similarity'], reverse=True)


def perform_text_similarity(sitc_title: str, oeance_title: str, should_extend_sitc: bool = False,
                            sitc_extensions: List[str] = None):
    if not should_extend_sitc:
        return text_similarites(sitc_title, oeance_title)
    else:
        # be very optimistic and assume that text similarity value equals the maximum similarity in case of extended
        # sitc values
        return max([text_similarites(sitc_extension, oeance_title) for sitc_extension in sitc_extensions])


@click.command()
@click.option('-e', '--use_enriched_sitc', required=True, is_flag=True, default=False)
@click.option('-v', '--verbose', required=True, is_flag=True, default=False)
def main(use_enriched_sitc: bool, verbose: bool):
    oenace_codes = load_csv(OENACE_FILE_PATH)
    sitc_codes = load_csv(SITC2_FILE_PATH)
    sitc_enriched_codes = load_enriched_sitc_codes(SITC2_ENRICHED_FILE_PATH)

    method = 'stemming'
    metadata = load_metadata(method)

    counter = 0
    total = 0
    oenace_candidates = {}

    for sitc_code, sitc_title in sitc_codes.items():
        total += 1

        if total > 2:
            break

        if verbose:
            print(f"Findind a mapping for: '{sitc_title}'")

        sitc_title_extendend = [sitc_title]

        # if we want to use enriched version from the correspondence tables, extend sitc titles
        if use_enriched_sitc:
            extending = sitc_enriched_codes.get(sitc_code, [])

            if extending and verbose:
                print(f'Extending "{sitc_title}" with: {extending}')

            sitc_title_extendend += extending

        # hold a list of possible mapping candidates from oenace codes for each method
        oenace_candidates[sitc_code] = {
            'text_similarity': [],
            'inverted_index': [],
        }
        # step1: try to do exact name matching
        for oenace_code, oenace_title in oenace_codes.items():
            text_similarity = perform_text_similarity(
                sitc_title=sitc_title, oeance_title=oenace_title, should_extend_sitc=use_enriched_sitc,
                sitc_extensions=sitc_title_extendend
            )

            if text_similarity > TEXT_SIMILARITY_THRESHOLD:
                oenace_candidates[sitc_code]['text_similarity'].append({
                    'oenace_code': oenace_code,
                    'oenace_title': oenace_title,
                    'similarity': text_similarity,
                })

        # sort by text similiarty desc, keeping the best matching oenace code first
        if oenace_candidates[sitc_code]['text_similarity']:
            oenace_candidates[sitc_code]['text_similarity'] = sort_by_similarity(oenace_candidates[sitc_code]['text_similarity'])

        # step2: perform search using tf-idf weighting
        tf_idf_results = perform_exploration(query='.'.join(sitc_title_extendend), method=method, metadata=metadata)
        if tf_idf_results:
            oenace_candidates[sitc_code]['inverted_index'].extend([{
                'oenace_code': item[0],
                'oenace_title': oenace_codes[item[0]],
                'similarity': item[1],
            } for item in tf_idf_results])

        # step 4: a model

        # pprint(oenace_candidates)

        # find intersections from all steps
        intersections = find_matching_intersections(oenace_candidates[sitc_code])

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

    click.echo(f'Found a total of {counter} mappings from {total}')
    start_gui(sitc_codes=sitc_codes, oeance_codes=oenace_codes, oenace_candidates=oenace_candidates)


if __name__ == '__main__':
    main()
