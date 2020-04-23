# SITC to OENACE mapper

An automated mapper from SITC (Standard International Trade Classification) to ÖNACE 
(Austrian nomenclature used for all industries and service activities).

## Setup

Install requirements via:

`pip install -r requirements.txt`


In order to run the project, please mark 'src' folder as sources root (if you use PyCharm as IDE, it should do that 
automatically), download the needed pre-trained word embedded model (see the README under `data` on how to do it) and 
then run the script `sitc_to_oenace_mapper.py`:

```
python src/sitc_to_oenace_mapper.py
```
### Used approach

The mapping procedure has three main steps:

* Fuzzy matching based on the description of categories
* TF-IDF weighting
* Word Embedding

The mapper runs the mapping procedure and then shows a GUI for the user, where mappings can be altered as needed.


### Troubleshooting

If tkinter does not work, install python3-tk via (tested on ubuntu only):

`sudo apt-get install python3-tk`