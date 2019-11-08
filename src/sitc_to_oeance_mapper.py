from fuzzywuzzy import fuzz

from inverted_index.querying import perform_exploration
from src.utils import load_csv
from inverted_index.utils import load_metadata

OENACE_FILE_PATH = '../data/raw/oenace2008.csv'
SITC2_FILE_PATH = '../data/raw/sitc2.csv'


def text_similarites(text1: str, text2: str) -> int:
    # TODO: add more explanations of what this does from. Use https://github.com/seatgeek/fuzzywuzzy
    val = fuzz.token_set_ratio(text1, text2)
    # print(f'Similiartiy between {text1} and {text2} is: {val}')
    return val


def main():
    oenace_codes = load_csv(OENACE_FILE_PATH)
    sitc_codes = load_csv(SITC2_FILE_PATH)

    # for sitc_code in sitc_codes:
    #     # hold a list of possible mapping candidates from oenace codes
    #     oenace_candidates = []
    #
    #     for oenace_code in oenace_codes[:10]:
    #         text_similarity = text_similarites(sitc_code['title'], oenace_code['title'])
    #
    #         if text_similarity == 100:
    #             print(23)
    #         if text_similarity > 70:
    #             oenace_candidates.append({
    #                 'oenace_code': oenace_code,
    #                 'similarity': text_similarity,
    #             })
    #     if oenace_candidates:
    #         print(f'Candidates for "{sitc_code["title"]}"')
    #         for cand in oenace_candidates:
    #             print(f'\t Similarity: {cand["similarity"]}, OENACE value: "{cand["oenace_code"]["title"]}"')

    method = 'stemming'
    metadata = load_metadata(method)

    for sitc_code in sitc_codes:
        results = perform_exploration(query=sitc_code['title'], method=method, metadata=metadata)
        print(results)


if __name__ == '__main__':
    main()
