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


@click.command()
@click.option('-v', '--verbose', required=True, is_flag=True, default=False)
def main(verbose: bool):
    oenace_codes = load_csv(OENACE_FILE_PATH)
    sitc_codes = load_csv(SITC2_FILE_PATH)
    sitc_enriched_codes = load_enriched_sitc_codes(SITC2_ENRICHED_FILE_PATH)

    results = []

    for use_enriched_sitc in [True, False]:
        for method in ['lemmatizing', 'stemming']:
            metadata = load_metadata(method)

            counter = 0
            total = 0
            oenace_candidates = {}

            for sitc_code, sitc_title in sitc_codes.items():
                total += 1

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

                # step2: perform search using tf-idf weighting
                tf_idf_results = perform_exploration(query='.'.join(sitc_title_extendend), method=method, metadata=metadata)
                if tf_idf_results:
                    oenace_candidates[sitc_code]['inverted_index'].extend([{
                        'oenace_code': item[0],
                        'oenace_title': oenace_codes[item[0]],
                        'similarity': item[1],
                    } for item in tf_idf_results])

            total_mapped = 0
            length_of_mapped_items = 0
            for sitc_code in oenace_candidates.keys():
                if oenace_candidates[sitc_code].get('inverted_index'):
                    total_mapped += 1
                    length_of_mapped_items += len(oenace_candidates[sitc_code]['inverted_index'])

            results.append({
                'method': method,
                'enriched': use_enriched_sitc,
                'total_mapped_pct': round((total_mapped / len(sitc_codes)) * 100, 2),
                'avg_length': round(length_of_mapped_items / total_mapped, 2)
            })

    import csv
    SITC_PATH_PREPROCESSED = '../data/chart_results/lemavsstem.csv'
    with open(SITC_PATH_PREPROCESSED, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['method', 'enriched', 'total_mapped_pct', 'avg_length'])
        writer.writeheader()
        writer.writerows(results)

    print(23)



if __name__ == '__main__':
    main()
