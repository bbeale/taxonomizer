from fuzzywuzzy import fuzz
from fuzzywuzzy import string_processing
from fuzzywuzzy import process
from Levenshtein import *
import difflib
import csv
import pymssql

print CompareTaxonomyNodes("Bird Cages", "Bird houses")

# need to revisit this function because it is not recycling for the next pub_tax
def CompareTaxonomies(st, ls):
    st_ = st[2].split("|")
    endnode = st_[-1].rstrip().lower()
    matches = []
    for item in ls:
        item_ = item[1].split("|")
        gnode = item_[-1].rstrip().lower()

        score = fuzz.WRatio(endnode, gnode)

        result = [[score], st, item]
        if score >= 50:
            matches.append(result)
        
    matches.sort(reverse=True)
    #pair = matches.pop()
    #matches = None
    print type(matches)
    print matches[0]
    return matches