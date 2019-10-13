import requests
DANDELION_URL = 'https://api.dandelion.eu/datatxt/sim/v1/'
DANDELION_TOKEN = 'dbec714ae95448a18d16ae355fe2a52d'


def find_similarity(text1: str, text2: str) -> int:
    response = requests.get(DANDELION_TOKEN, params={'text1': text1, 'text2': text2, 'token': DANDELION_TOKEN})
    # TODO: check the response on rate limits
    response.raise_for_status()
    return response.json()['similarity']
