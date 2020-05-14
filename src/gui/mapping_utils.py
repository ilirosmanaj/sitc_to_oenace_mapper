import pickle
from pathlib import Path

PATH_TO_MAPPING = '../data/candidates_results'


class CandidatesHandler:
    def __init__(self):
        self.path_to_results = PATH_TO_MAPPING

    def store_candidates(self, oenace_candidates: dict, file_name: str):
        full_path = f'{self.path_to_results}/{file_name}.pkl'

        with open(Path(full_path), 'wb') as f:
            pickle.dump(oenace_candidates, f, pickle.HIGHEST_PROTOCOL)

        return True

    def load_candidates(self, file_name: str) -> dict:
        file_name = file_name.replace('.csv', '.pkl').replace('mapping_results', 'candidates_results')
        with open(Path(file_name), 'rb') as f:
            return pickle.load(f)
