# SITC to OENACE mapper

An automated mapper from SITC (Standard International Trade Classification) to ÖNACE 
(Austrian nomenclature used for all industries and service activities).

## Setup

##### Create a virtual environment to install the needed requirements and activate it:

```
python -m virtualenv venv
source venv/bin/activate
```

##### Install requirements via:

`pip install -r requirements.txt`

##### Download needed packages from nltk

You can run this from python console:

```{python}
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('stopwords')
```

##### Download the pretrained word embedded model

See the README under `data` on how to do it
 
##### Build the inverted indexes

Build the inverted index by running the `build_inverted_index.py` under the `src/inverted_index` folder
    
* Do this for both methods: stemming and lemmatizing
* this should store the inverted index files under `data/inverted_index`

##### Run the mapper

Run the `sitc_to_oenace_mapper.py` script via

```
python src/sitc_to_oenace_mapper.py
```

### Used approach

The mapping procedure has three main steps:

* Fuzzy matching based on the description of categories
* TF-IDF weighting
* Word Embedding

The mapper runs the mapping procedure and then displays a GUI to the user, where mappings can be altered (if needed).


### Troubleshooting

If tkinter does not work, install python3-tk via (tested on ubuntu only):

`sudo apt-get install python3-tk`
