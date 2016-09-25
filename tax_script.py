from fuzzywuzzy import fuzz
from fuzzywuzzy import string_processing
from fuzzywuzzy import process
from Levenshtein import *
import difflib
import csv
import pymssql

def CompareTaxonomyNodes(p, g):

    score = fuzz.WRatio(p, g)

    if score >= 50:
        return True

def ExtractFirst(array):
    array.sort(key=lambda a: int(a[1]), reverse=True)
    return array[0]

root = "C:\\Users\\bbeale\\Documents\\Visual Studio Code\\dataops\\" 

google_taxonomies = open(root + "testfiles\\googletaxonomy.csv", "r")
pub_taxonomies = open(root + "testfiles\\officedepot_taxonomies_test.csv", "r")
#temp = open(root + "results\\temp.csv", "r+")

google_taxonomies_ = csv.reader(google_taxonomies, delimiter=',', lineterminator='\n')
pub_taxonomies_ = csv.reader(pub_taxonomies, delimiter=',', lineterminator='\n')
#temp_ = csv.writer(temp, delimiter=',', lineterminator='\n')

# if client name is given 
toprow = ["clientid", "name", "Publisher taxonomyid", "Publisher taxonomytext", "globaltaxonomyid", "Global taxonomytext", "score"]
# if just clientid is given
toprow_ = ["clientid", "Publisher taxonomyid", "Publisher taxonomytext", "globaltaxonomyid", "Global taxonomytext", "score"]

#temp_.writerow(toprow_)

for p in pub_taxonomies_:
    p_ = p[2].split("|")
    endnode = p_[-1].rstrip().lower()
    best = ["NULL", "NULL"]
    score = 0
    matches = [p, best, score]

    for g in google_taxonomies_:
        g_ = g[1].split("|")
        gnode = g_[-1].rstrip().lower()
        if CompareTaxonomyNodes(endnode, gnode):
            if fuzz.WRatio(endnode, gnode) > score:
                best = g
                score = fuzz.WRatio(endnode, gnode)
            res = [matches[0], best, score]
    final = open(root + "results\\mapped.csv", "w")
    final_ = csv.writer(final, delimiter=',', lineterminator='\n')
    final_.writerow(toprow_)
    final_.writerow(res)
    final.close()
google_taxonomies.close()
pub_taxonomies.close()
#temp.close()