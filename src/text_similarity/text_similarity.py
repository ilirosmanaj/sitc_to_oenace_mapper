from typing import List
from fuzzywuzzy import fuzz


def text_similarites(text1: str, text2: str, verbose: bool = False) -> int:
    """Perform a token set ration similarity comparison"""
    val = fuzz.token_set_ratio(text1, text2)
    if verbose:
        print(f'Similiartiy between {text1} and {text2} is: {val}')
    return val


def perform_text_similarity(sitc_title: str, oeance_title: str, should_extend_sitc: bool = False,
                            sitc_extensions: List[str] = None):
    if not should_extend_sitc:
        return text_similarites(sitc_title, oeance_title)
    else:
        # be very optimistic and assume that text similarity value equals the maximum similarity in case of extended
        # sitc values
        return max([text_similarites(sitc_extension, oeance_title) for sitc_extension in sitc_extensions])

