from inverted_index.preprocessing import pre_process
from inverted_index.scoring import tf_idf
from inverted_index.utils import load_metadata


def perform_exploration(query: str, method: str, metadata: dict):
    # preprocess query into terms
    query_terms = pre_process(query, method)

    # read stuff from metadata
    inverted_index = metadata['inverted_index']
    number_of_documents = metadata['number_of_documents']

    scores = {}

    for i, term in enumerate(query_terms):

        # if inverted index has no trace for the given term, skip it
        if term not in inverted_index:
            continue

        posting_list = inverted_index[term]

        for doc_id, term_frequency in posting_list:
            if doc_id not in scores:
                scores[doc_id] = 0

            scores[doc_id] += tf_idf(term_frequency=term_frequency,
                                     number_of_documents=number_of_documents,
                                     posting_list=posting_list)

    # return sorted dictionary by score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]


def main():
    method = 'stemming'
    metadata = load_metadata(method)
    query = 'test'
    results = perform_exploration(query=query, method=method, metadata=metadata)

    # Shitty output
    print('\n\nQuerying for "{}" revealed the following results:'.format(query))
    for doc_id, score in results:
        print('     Document_id: {}, Score: {}'.format(doc_id, score))
    print('\n\n')


if __name__ == '__main__':
    main()
