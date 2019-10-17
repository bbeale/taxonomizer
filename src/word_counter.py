from dataops import taxonomizer
from fuzzywuzzy import fuzz
from Levenshtein import *
import datetime, csv




# filename
fname = "FNAC 2"

#index = -2


# set file path names
desktop = "C:\\Users\\bbeale\\Desktop\\"

mappings = open(desktop + fname + ".csv", "r")
countsheet = open(desktop + "taxonomy_outputs\\" + fname + " - Word Count.csv", "w")

mappings_ = csv.reader(mappings, delimiter=',', lineterminator='\n')
countsheet_ = csv.writer(countsheet, delimiter=',', lineterminator='\n')

toprow = ["word", "count"]
temp = []
countsheet_.writerow(toprow)

for m in mappings_:
    #pt = taxonomizer.get_unique_taxonomy_words(m[3])
    #print "PT: ", pt
    pt_ = m[3].split("|")
    print "pt_: ", pt_
    for item in pt_: #.split():
        temp.append(item) 

counter, max = taxonomizer.GetMostFrequentWord(temp)


for key, value in counter.items():
    print "The word ", key, " occurred ", value, " times."
    countsheet_.writerow([key, value])
    
countsheet_.writerow(["Most frequent word: ", max])

mappings.close()
countsheet.close()