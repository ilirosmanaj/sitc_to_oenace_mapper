import click
from typing import Dict

from utils import find_matching_intersections

PATH_TO_RESULTS = '../data/mapping_results/'


def _input_is_yes(input_str: str):
    return input_str in ['Y', 'y']


def _store_best_candidates():
    pass


def _filter_oeance_candidates(oeance_candidates):
    """Perform some filtering based on some query"""
    pass


def search_manually(oeance_candidates: Dict):
    click.echo('Please type the id or the title of the oeance code')
    response = input()
    # start doing something filthy here


def cli(sitc_codes: Dict, oeance_codes: Dict, oeance_candidates: Dict, mapped_count: int):
    click.echo(f'Do you want to continue with manual mapping or use best matching candidates '
               f'(a total of {mapped_count})? [y] or [n]')
    response = input()

    mapping = {}
    if not _input_is_yes(response):
        _store_best_candidates()
        click.echo('Stored the best candidates from what the automated process. Exiting now!')
        return

    # iterate through each sitc_code and offer the user the option of choosing either an element from the intersection
    # list, or manually choose one
    for sitc_code, sitc_title in sitc_codes.items():
        intersections = find_matching_intersections(oeance_candidates[sitc_code])

        click.echo(f'Finding a mapping for {sitc_code} - "{sitc_title}"')

        if intersections:
            candidate_chosen = False

            while not candidate_chosen:
                click.echo('The list of intersections available:')

                # offer the user with the list of intersections
                for i, val in enumerate(intersections):
                    click.echo(f'\t {i+1}. {val}')

                click.echo('Click the candidate number if you want to chose one of them, or click Y to continue '
                           'searching manually:')
                response = input()

                if isinstance(response, int):
                    if 0 < response < len(intersections):
                        choice = intersections[response-1]
                        candidate_chosen = True
                        break
                    else:
                        click.echo('Please choose one of the offered candidates, not other numbers')
                else:
                    choice = search_manually(oeance_codes)
        else:
            choice = search_manually()
