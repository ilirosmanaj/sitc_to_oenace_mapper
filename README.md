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
*** apparently there is a Dandelion API for text similarity
* if matching by description is not good enough, try corresponding table 
* build a model that would find similarities between categories, and if no good 
category is found, use it to find the _most fitting_ category 