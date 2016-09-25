from fuzzywuzzy import fuzz
from Levenshtein import *
import difflib
import csv

root = "C:\\Users\\bbeale\\Documents\\Visual Studio Code\\dataops\\"

mappings = open(root + "testfiles\\officedepotelectronics.csv", "r")
reviewed = open(root + "results\\ODE_scored.csv", "w")

mappings_ = csv.reader(mappings, delimiter=',', lineterminator='\n')
reviewed_ = csv.writer(reviewed, delimiter=',', lineterminator='\n')

for m in mappings_:
    pt = m[3].rstrip().split("|")
    gt = m[5].rstrip().split("|")

    pt_ = pt[-1].lower()
    gt_ = gt[-1].lower() 

    dist = fuzz.WRatio(pt_, gt_)

    if dist > 70:
        reviewed_.writerow([m[0], m[1], m[2], m[3], m[4], m[5]])
    elif dist > 50:
        reviewed_.writerow([m[0], m[1], m[2], m[3], m[4], m[5], "near"])
    else:
        reviewed_.writerow([m[0], m[1], m[2], m[3], m[4], m[5], "far"])

mappings.close()
reviewed.close()