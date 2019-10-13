# SITC to OENACE mapper

An automated mapper from SITC (Standard International Trade Classification) to ÖNACE 
(Austrian nomenclature used for all industries and service activities).

## Setup

Install requirements via:

`pip install -r requirements.txt`

### Used approach

The mapping procedure has three main steps:

* fuzzy matching based on the description of categories
** think of incorporating semantic meaning as well (try some NLP approach)
* if matching by description is not good enough, try corresponding table 
* build a model that would find similarities between categories, and if no good 
category is found, use it to find the _most fitting_ category 

### To research

* [Dandelion API](https://dandelion.eu/) for the NLP approach
    * works relatively fine, but its quite expensive. For us, if we would use the brute-force approach of comparing
      all_sitc with all_oenace would be around 4 milion requets for every category. A load like this is not even supported
      by their offers (neither free nor paid).
    * As part of this, a bunch of other text similarity API-s were considered (e.g. [Parallel Dots](https://www.paralleldots.com/), 
     [TwinWord](https://www.twinword.com/api/text-similarity.php), [RxNLP](https://rxnlp.com/text-similarity-api/#.XaL5uuYzY5k)),
     but all of them are too expensive for use.
* find if there is a model that finds similarities between different product 
  categories 