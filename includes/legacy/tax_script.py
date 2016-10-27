from dataops import taxonomizer
from fuzzywuzzy import fuzz
import csv, datetime








# filename 
fname =  "TescoDirect2 - RERUN"  #"algo_test_files\\TEST" #

# threshold
threshold = 85








# set file path names
root = "C:\\Users\\bbeale\\Documents\\VisualStudioCode\\dataops\\" 
desktop = "C:\\Users\\bbeale\\Desktop\\"

# open publisher tax file, create csv reader object
pub_taxonomies = open(desktop + fname + ".csv", "r")

pub_taxonomies_ = csv.reader(pub_taxonomies, delimiter=',', lineterminator='\n')

# if client name is given  
toprow = ["ClientId", "Name", "PublisherTaxonomyId", "PublisherTaxonomyText", "GlobalTaxonomyId", "GlobalTaxonomyText", "Distance"]

# create output file, write top row
final = open(desktop + fname + " - BETA - " + str(datetime.datetime.now().date()) + ".csv", "w")
final_ = csv.writer(final, delimiter=',', lineterminator='\n')
final_.writerow(toprow)

rerun = open(desktop + fname + " - RERUN THIS LIST - " + str(datetime.datetime.now().date()) + ".csv", "w")
rerun_ = csv.writer(rerun, delimiter=',', lineterminator='\n')

# Number of complete mappings
match_count = 0

# compare end nodes for each publisher taxonomy to end nodes for each google taxonomy, write list of best
# matching google taxonomies to publisher taxonomies, scored with wratio(), to a new csv
for p in pub_taxonomies_:

    p_ = p[3].split("|")  
        
    endnode = p_[-1].rstrip().lower() 

    best = ["NULL", "NULL"]
    score = 0

    google_taxonomies = open(root + "includes\\googletaxonomy.csv", "r")
    google_taxonomies_ = csv.reader(google_taxonomies, delimiter=',', lineterminator='\n')

    for g in google_taxonomies_:

        g_ = g[1].split("|")
        gnode = g_[-1].rstrip().lower()




        ## ADJUST THE PART OF THE TAXONOMY TO COMPARE

        # grab unique words and use partial ratio if more than 3 nodes
        #if len(p_) > 3:

            #endnode_ = p_[-2].strip().lower() + " " + p_[-1].rstrip().lower() 
            #endnode = taxonomizer.GetUniqueTaxonomyWords(endnode_)
            #gnode = taxonomizer.GetUniqueTaxonomyWords(g[1]).lower()

            # might have to move this block back left
            #if taxonomizer.CompareTaxonomyPartialRatio(endnode, gnode, threshold):
            #    if fuzz.partial_ratio(endnode, gnode) > score:
            #        best = g
            #        score = fuzz.partial_ratio(endnode, gnode) > score


            # if the above doesn't catch anything:
            #endnode = p_[-2].strip().lower()





        if taxonomizer.CompareTaxonomyNodes(endnode, gnode, threshold):
        #if taxonomizer.CompareTaxonomyPartialRatio(endnode, gnode, threshold):
            if fuzz.WRatio(endnode, gnode) > score:
            #if fuzz.partial_ratio(endnode, gnode) > score:
                best = g
                score = fuzz.WRatio(endnode, gnode)

        clientid = p[0]
        name = p[1]
        taxonomyid = p[2]
        taxonomytext = p[3]

    if score > threshold:
        matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], taxonomizer.SetReviewLevel(score)]
        final_.writerow(matches)
        match_count += 1
        print match_count, " matches so far"
        #print "Match! ", matches
    else:
        temp_list = [clientid, name, taxonomyid, taxonomytext, "NULL", "NULL", "Far"]
        rerun_.writerow(temp_list)

    google_taxonomies.close()

pub_taxonomies.close()
final.close()
