"""Common pre-processing script. Used for document and query pre-processing"""
import re
from typing import List
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

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
              'wouldn', "wouldn't"]

# starting quotes
STARTING_QUOTES = [
    (re.compile(r'^\"'), r'``'),
    (re.compile(r'(``)'), r' \1 '),
    (re.compile(r"([ \(\[{<])(\"|\'{2})"), r'\1 `` '),
]

# punctuation
PUNCTUATION = [
    (re.compile(r'([:,])([^\d])'), r' \1 \2'),
    (re.compile(r'([:,])$'), r' \1 '),
    (re.compile(r'\.\.\.'), r' ... '),
    (re.compile(r'[;@#$%&]'), r' \g<0> '),
    (
        re.compile(r'([^\.])(\.)([\]\)}>"\']*)\s*$'),
        r'\1 \2\3 ',
    ),  # Handles the final period.
    (re.compile(r'[?!]'), r' \g<0> '),
    (re.compile(r"([^'])' "), r"\1 ' "),
]

# Pads parentheses
PARENS_BRACKETS = (re.compile(r'[\]\[\(\)\{\}\<\>]'), r' \g<0> ')

DOUBLE_DASHES = (re.compile(r'--'), r' -- ')

# ending quotes
ENDING_QUOTES = [
    (re.compile(r'"'), " '' "),
    (re.compile(r'(\S)(\'\')'), r'\1 \2 '),
    (re.compile(r"([^' ])('[sS]|'[mM]|'[dD]|') "), r"\1 \2 "),
    (re.compile(r"([^' ])('ll|'LL|'re|'RE|'ve|'VE|n't|N'T) "), r"\1 \2 "),
]


def pre_process(text: str, method: str = None) -> List[str]:
    """
    Pre-processes a text: pipelining through tokenization, lowercasing, removing stopwords and more - depending on the
    chosen method
    """
    line = text

    # basic processing steps
    processing_steps = [_tokenize, _lowercase, _remove_stop_words]

    if method == 'stemming':
        processing_steps.append(_stemm)
    elif method == 'lemmatizing':
        processing_steps.append(_lemmatize)
    elif method == 'all':
        processing_steps.extend([_stemm, _lemmatize])

    for processing_step in processing_steps:
        line = processing_step(line)

    return line


def _tokenize(text: str) -> List[str]:
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(text)


def _lowercase(text: List[str]) -> List[str]:
    return list(map(lambda x: x.lower(), text))


def _remove_stop_words(text: List[str]) -> List[str]:
    valid_words = []
    for item in text:
        if item not in STOP_WORDS:
            valid_words.append(item)

    return valid_words


def _stemm(text: List[str]) -> List[str]:
    stemmed_words = set()
    porter_stemmer = PorterStemmer()
    for word in text:
        stemmed_words.add(porter_stemmer.stem(word))

    return list(stemmed_words)


def _lemmatize(text: List[str]) -> List[str]:
    lemmatized_words = set()
    wordnet_lemmatizer = WordNetLemmatizer()
    for word in text:
        lemmatized_words.add(wordnet_lemmatizer.lemmatize(word))

    return list(lemmatized_words)
