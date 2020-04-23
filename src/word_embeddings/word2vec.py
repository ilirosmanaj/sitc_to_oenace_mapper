from math import inf
from typing import List

from nltk.corpus import stopwords
from gensim.models import KeyedVectors
from nltk import word_tokenize

stop_words = stopwords.words('english')

PATH_TO_PRETRAINED_MODEL = '../data/word_embedding/GoogleNews-vectors-negative300.bin.gz'
INF_SIMILIARITY = 100000000


class Word2VecSimilarity:
    def __init__(self, verbose: bool):
        self.model = KeyedVectors.load_word2vec_format(PATH_TO_PRETRAINED_MODEL, binary=True, limit=5000)
        self.model.init_sims(replace=True)

        self.verbose = verbose

    def _pre_process(self, sentence: str):
        doc = word_tokenize(sentence.lower())
        doc = [w for w in doc if w not in stop_words]

        #self.model.cosine_similarities()
        return doc

    def text_similarity(self, text_1: str, text_2: str):
        """Returns the word movers distance between two strings"""
        txt1 = self._pre_process(text_1)
        txt2 = self._pre_process(text_2)

        sim = self.model.wmdistance(txt1, txt2)

        if sim == inf:
            sim = INF_SIMILIARITY
        return sim

    def enriched_sitc_similarity(self, enriched_sitc: List[str], oenace_title: str):
        """
        Used when enriched_sitc is enabled.

        Finds the word movers distance of each enriched_sitc version with the oenace title, and returns the smallest one
        (this case we're being optimistic)
        """
        # assume we are performing really bad in the beginning
        min_similarity = INF_SIMILIARITY

        # iterate through all enriched versions of sitc and compare their similarity with the oenace title
        # as results, return the smallest distance
        for sitc in enriched_sitc:

            similarity = self.text_similarity(sitc, oenace_title)

            # we already found something better, use that
            if similarity < min_similarity:
                min_similarity = similarity

        return min_similarity
