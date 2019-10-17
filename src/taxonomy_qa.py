from fuzzywuzzy import fuzz
from Levenshtein import *
import datetime
import difflib
import csv

## be sure to make sure column headers line up and remove them from the 
## spreadsheet before feeding into this script
fname = "bboo"

# set file path names
desktop = "C:\\Users\\bbeale\\Desktop\\"

mappings = open(desktop + fname + ".csv", "r")
reviewed = open(desktop + fname + " - SCORED - " + str(datetime.datetime.now().date()) + ".csv", "w")

mappings_ = csv.reader(mappings, delimiter=',', lineterminator='\n')
reviewed_ = csv.writer(reviewed, delimiter=',', lineterminator='\n')

# if client name is given  
toprow = ["clientid", "name", "Publisher taxonomyid", "Publisher taxonomytext", "globaltaxonomyid", "Global taxonomytext", "Distance"]
# if just clientid is given
toprow_ = ["clientid", "Publisher taxonomyid", "Publisher taxonomytext", "globaltaxonomyid", "Global taxonomytext", "Distance"]

reviewed_.writerow(toprow_)

for m in mappings_:
    pt = m[2].rstrip().split("|")
    gt = m[4].rstrip().split("|")

    pt_ = pt[-1].lower()
    gt_ = gt[-1].lower() 

    dist = fuzz.WRatio(pt_, gt_)

    if dist > 80: # Adjsut as needed
        reviewed_.writerow([m[0], m[1], m[2], m[3], m[4], "Exact"])
    elif dist > 50:
        reviewed_.writerow([m[0], m[1], m[2], m[3], m[4], "Near"])
    else:
        reviewed_.writerow([m[0], m[1], m[2], m[3], m[4], "Far"])

mappings.close()
reviewed.close()