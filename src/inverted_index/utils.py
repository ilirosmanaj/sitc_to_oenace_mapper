import pickle
from statistics import mean
from pathlib import Path


STOP_WORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
              'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
              'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
              'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were',
              'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
              'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
              'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
              'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
              'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
              'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
              'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain',
              'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn',
              "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
              "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't",
              'wouldn', "wouldn't", "i.e."]

METHODS = ['basic_package', 'stemming', 'lemmatizing', 'all']

# store metadata files under data/metadata folder
PATH_TO_METADATA = '../data/inverted_index/inverted_index_{}.pkl'


def save_metadata(method: str, inverted_index: dict, documents: dict):
    """
    Saves inverted index and document metadata as dictionary.

    Method is one of ['basic_package', 'stemming' , 'lemmatizing']. Used to not overwrite the
    stored metadata/inverted index.
    """
    if method not in METHODS:
        raise ValueError('Method unknown. Use one of [basic_package, stemming, lemmatizing]')

    filename = PATH_TO_METADATA.format(method)
    with open(Path(filename), 'wb') as f:
        pickle.dump({
            'inverted_index': inverted_index,
            'avg_document_length': mean([len(doc_words) for doc_id, doc_words in documents.items()]),
            'document_lengths': {doc_id: len(doc_words) for doc_id, doc_words in documents.items()},
            'number_of_documents': len(documents.keys())
        }, f, pickle.HIGHEST_PROTOCOL)

    print('Saved metadata file as {}'.format(filename))


def load_metadata(method: str) -> dict:
    print(f'Loading metadata for method {method}')
    if method not in METHODS:
        raise ValueError('Method unknown. Use one of [basic_package, stemming, lemmatizing]')

    with open(Path(PATH_TO_METADATA.format(method)), 'rb') as f:
        return pickle.load(f)

