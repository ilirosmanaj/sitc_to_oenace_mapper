from fuzzywuzzy import fuzz
from src.utils import load_csv

OENACE_FILE_PATH = '../data/oenace2008.csv'
SITC2_FILE_PATH = '../data/sitc2.csv'


def text_similarites(text1: str, text2: str) -> int:
    # TODO: add more explanations of what this does from. Use https://github.com/seatgeek/fuzzywuzzy
    return fuzz.token_set_ratio(text1, text2)


def main():
    oenace_codes = load_csv(OENACE_FILE_PATH)
    sitc_codes = load_csv(SITC2_FILE_PATH)

    for sitc_code in sitc_codes:
        # hold a list of possible mapping candidates from oenace codes
        oenace_candidates = []

        for oenace_code in oenace_codes:
            text_similarity = text_similarites(sitc_code['title'], oenace_code['title'])

            if text_similarity > 60:
                oenace_candidates.append({
                    'oenace_code': oenace_code,
                    'similarity': text_similarity,
                })
        print("\n")
        if oenace_candidates:
            print(f'Candidates for "{sitc_code["title"]}"')
            for cand in oenace_candidates:
                print(f'\t Similarity: {cand["similarity"]}, OENACE value: "{cand["oenace_code"]["title"]}"')
        else:
            print(f'Did not find any mapping to oenace for "{sitc_code["title"]}"')


if __name__ == '__main__':
    main()
