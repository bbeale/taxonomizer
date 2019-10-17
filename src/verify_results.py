#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fuzzywuzzy import fuzz
from Levenshtein import *
import datetime
import difflib
import csv
import os

## be sure to make sure column headers line up and remove them from the 
## spreadsheet before feeding into this script
fname = "bboo"

# set file path names
datadir = os.path.relpath("data")
outputdir = os.path.relpath("output")

mappings = open(output_dir + fname + ".csv", "r")
reviewed = open(output_dir + fname + " - SCORED - " + str(datetime.datetime.now().date()) + ".csv", "w")

mappings_ = csv.reader(mappings, delimiter=',', lineterminator='\n')
reviewed_ = csv.writer(reviewed, delimiter=',', lineterminator='\n')

# if client name is given  
toprow = ["clientid", "name", "Publisher taxonomyid", "Publisher taxonomytext", "globaltaxonomyid", "Global taxonomytext", "Distance"]
# if just clientid is given
toprow_ = ["clientid", "Publisher taxonomyid", "Publisher taxonomytext", "globaltaxonomyid", "Global taxonomytext", "Distance"]

reviewed_.writerow(toprow_)

for m in mappings_:
    pt = m[2].rstrip().split("|")[-1].lower()
    gt = m[4].rstrip().split("|")[-1].lower()

    # pt_ = pt[-1].lower()
    # gt_ = gt[-1].lower()

    dist = fuzz.WRatio(pt, gt)

    distance = None
    if dist > 80:  # Adjsut as needed
        distance = "exact"
    elif dist > 50:
        distance = "near"
    else:
        distance = "far"

    reviewed_.writerow([m[0], m[1], m[2], m[3], m[4], distance])

mappings.close()
reviewed.close()