import click

from gui.gui import start_gui
from inverted_index.querying import perform_exploration
from src.utils import load_csv, load_enriched_sitc_codes, find_matching_intersections, sort_by_similarity
from inverted_index.utils import load_metadata
from text_similarity.text_similarity import perform_text_similarity
from word_embeddings.word2vec import Word2VecSimilarity

OENACE_FILE_PATH = '../data/preprocessed/oenace2008.csv'
SITC2_FILE_PATH = '../data/preprocessed/sitc2.csv'
SITC2_ENRICHED_FILE_PATH = '../data/correspondence_tables/mapped/enriched.csv'

TEXT_SIMILARITY_THRESHOLD = 65


@click.command()
@click.option('-e', '--use_enriched_sitc', required=True, is_flag=True, default=True)
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

        if total > 5:
            pass

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
            'word_embedding': [],
        }

        # step1: try to do exact name matching
        for oenace_code, oenace_title in oenace_codes.items():
            text_similarity = perform_text_similarity(
                sitc_title=sitc_title, oeance_title=oenace_title,
                should_extend_sitc=use_enriched_sitc,
                sitc_extensions=sitc_title_extendend
            )

            if text_similarity > TEXT_SIMILARITY_THRESHOLD:
                oenace_candidates[sitc_code]['text_similarity'].append({
                    'oenace_code': oenace_code,
                    'oenace_title': oenace_title,
                    'similarity': text_similarity,
                })

        # step2: perform search using tf-idf weighting
        tf_idf_results = perform_exploration(query='.'.join(sitc_title_extendend), method=method, metadata=metadata)
        if tf_idf_results:
            oenace_candidates[sitc_code]['inverted_index'].extend([{
                'oenace_code': item[0],
                'oenace_title': oenace_codes[item[0]],
                'similarity': item[1],
            } for item in tf_idf_results])

        # step 3: word embedding
        word2vec_similarity = Word2VecSimilarity(verbose=verbose)

        for oenace_code, oenace_title in oenace_codes.items():

            if use_enriched_sitc:
                word_embedding_similarity = word2vec_similarity.enriched_sitc_similarity(sitc_title_extendend,
                                                                                         oenace_title)
            else:
                word_embedding_similarity = word2vec_similarity.text_similarity(sitc_title, oenace_title)

            # append all as possible candidates, but in the end choose only top 3 with minimum distance
            oenace_candidates[sitc_code]['word_embedding'].append({
                'oenace_code': oenace_code,
                'oenace_title': oenace_title,
                'similarity': word_embedding_similarity,
            })

        # sort by similiarity descending
        for method in ['text_similarity', 'inverted_index']:
            if oenace_candidates[sitc_code][method]:
                oenace_candidates[sitc_code][method] = sort_by_similarity(
                    oenace_candidates[sitc_code][method],
                    descending=True
                )
        oenace_candidates[sitc_code]['word_embedding'] = sort_by_similarity(
            oenace_candidates[sitc_code]['word_embedding'], descending=False
        )[:100]

        # find intersections from all steps
        intersections = find_matching_intersections(oenace_candidates[sitc_code])

        if intersections:
            counter += 1
            print(f"\nFindind a mapping for: '{sitc_title}'")
            for val in intersections:
                print(f' - {val}')
            print(end='\n\n')

        print(f'Done {total}/{len(sitc_codes)} so far')

    click.echo(f'Found a total of {counter} mappings from {total}')

    start_gui(sitc_codes=sitc_codes, oeance_codes=oenace_codes, oenace_candidates=oenace_candidates)


if __name__ == '__main__':
    main()
