# Correspondace table usage

Since we have a limited number of categories (615 of OENACE and 757 for SITC), we need to do add data from other sources
as well, in order for our mapping to be more accurate.

Here's where corresponding tables come into play. We find some corresponding tables that convert from/to SITC2, and gather
the words used by other systems to define the same things as SITC2 does (e.g. we can learn that cereal is used together 
with word wheat).
Hopefully, these new words will give us extra information, which will be used for text matching against OENACE descriptions.

The list of correspondance tables used:

* HS1992 - SITC2
* HS1996 - SITC2
* HS2002 - SITC2
* HS2007 - SITC2
* HS2012 - SITC2
* HS2017 - SITC2

Source: [https://unstats.un.org/unsd/trade/classifications/correspondence-tables.asp](https://unstats.un.org/unsd/trade/classifications/correspondence-tables.asp)

All these are converted using the `convert.py` script and the results are stored under `data/correspondance_tables/preprocseed`.