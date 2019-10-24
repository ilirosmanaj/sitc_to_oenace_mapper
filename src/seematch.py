from sematch.semantic.similarity import WordNetSimilarity
wns = WordNetSimilarity()

# Computing English word similarity using Li method
print(wns.word_similarity('dog is a pet', 'cat is not a pet', 'li'))