from fuzzywuzzy import fuzz
from fuzzywuzzy import string_processing
from fuzzywuzzy import process
from Levenshtein import *
import datetime
import difflib
import pymssql
import csv

def CompareTaxonomyNodes(p, g):
    score = fuzz.WRatio(p, g)
    if score >= 50:
        return True

def SetReviewLevel(score):
    if score >= 90: return "Exact"
    elif score >= 80: return "Near"
    else: return "Far"
    
## be sure to make sure column headers line up and remove them from the 
## spreadsheet before feeding into this script

# for ebay, need to see which taxonomies need to use the second from end node
# i.e. stuffed animals from toys|stuffed animals|hello kitty
#fname = "Test_eBay_pt_2"
fname = "Test_OfficeDepot_pt_2"

# set file path names
root = "C:\\Users\\bbeale\\Documents\\Visual Studio Code\\dataops\\" 
desktop = "C:\\Users\\bbeale\\Desktop\\"

# open publisher tax file, create csv reader object
pub_taxonomies = open(desktop + fname + ".csv", "r")
pub_taxonomies_ = csv.reader(pub_taxonomies, delimiter=',', lineterminator='\n')

# if client name is given  
toprow = ["clientid", "name", "Publisher taxonomyid", "Publisher taxonomytext", "globaltaxonomyid", "Global taxonomytext", "Distance"]
# if just clientid is given
toprow_ = ["clientid", "Publisher taxonomyid", "Publisher taxonomytext", "globaltaxonomyid", "Global taxonomytext", "Distance"]

# create output file, write top row
final = open(desktop + fname + " - MAPPED - " + str(datetime.datetime.now().date()) + ".csv", "w")
final_ = csv.writer(final, delimiter=',', lineterminator='\n')
final_.writerow(toprow_)

# compare end nodes for each publisher taxonomy to end nodes for each google taxonomy, write list of best
# matching google taxonomies to publisher taxonomies, scored with wratio(), to a new csv
for p in pub_taxonomies_:

    p_ = p[3].split("|")
    endnode = p_[-1].rstrip().lower()
    best = ["NULL", "NULL"]
    score = 0
    
    google_taxonomies = open(root + "testfiles\\googletaxonomy.csv", "r")
    google_taxonomies_ = csv.reader(google_taxonomies, delimiter=',', lineterminator='\n')

    for g in google_taxonomies_:

        g_ = g[1].split("|")
        gnode = g_[-1].rstrip().lower()

        if CompareTaxonomyNodes(endnode, gnode):

            if fuzz.WRatio(endnode, gnode) > score:

                best = g
                score = fuzz.WRatio(endnode, gnode)

        clientid = p[0]
        taxonomyid = p[2]
        taxonomytext = p[3]

    matches = [clientid, taxonomyid, taxonomytext, best[0], best[1], SetReviewLevel(score)]

    final_.writerow(matches)
    #print matches 
    google_taxonomies.close()

pub_taxonomies.close()
final.close()
