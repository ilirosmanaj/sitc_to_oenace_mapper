## Word Embedding

The word embedding file directory contains the Google News pretrained word2vec model. This model was trained using
around 3 million words and phrases in total.

In order to download it, so that the mapper can use it, please do the following:

``
cd data/word_embedding
wget -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
``

Remember that this is a huge file and can take quite long - depending on the internet speed.
