from math import log10
from typing import List


def tf_idf(term_frequency: int, number_of_documents: int, posting_list: List) -> float:
    """
    Calculates the tf_idf score for a given term in a document. Based on Lecture-01 Slides [47-54].

    :returns tf_idf score for term-document relation
    """
    number_of_documents_with_term_frequency = len(posting_list)

    # implements the tf-idf formula
    return log10(1 + term_frequency) * log10(number_of_documents / number_of_documents_with_term_frequency)
