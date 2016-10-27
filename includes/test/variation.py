from dataops import taxonomizer
from fuzzywuzzy import fuzz
import csv, datetime








# filename 
fname = r"TescoDirect3 - RERUN"  #"algo_test_files\\TEST" # 

# threshold
threshold = 98

ratio_threshold = 90








# set file path names
root = "C:\\Users\\bbeale\\Documents\\VisualStudioCode\\dataops\\" 
desktop = "C:\\Users\\bbeale\\Desktop\\"

# open publisher tax file 
pub_list = taxonomizer.AddFileContentsToList(desktop + fname + ".csv")

# open google tax file
google_list = taxonomizer.AddFileContentsToList(r"C:\Users\bbeale\Documents\VisualStudioCode\dataops\includes\googletaxonomy.csv")

# toprow for output file
toprow = ["ClientId", "Name", "PublisherTaxonomyId", "PublisherTaxonomyText", "GlobalTaxonomyId", "GlobalTaxonomyText", "Flag"]

# create output file, write top row
final = open(desktop + fname + " - VARIATION BETA - " + str(datetime.datetime.now().date()) + ".csv", "w")
final_ = csv.writer(final, delimiter=',', lineterminator='\n')
final_.writerow(toprow)

# generate file of misses to rerun
rerun = open(desktop + fname + " - VARIATION RERUN THIS LIST - " + str(datetime.datetime.now().date()) + ".csv", "w")
rerun_ = csv.writer(rerun, delimiter=',', lineterminator='\n')

# Number of complete mappings
match_count = 0
miss_count = 0

temp = []

# compare end nodes for each publisher taxonomy to end nodes for each google taxonomy, write list of best
# matching google taxonomies to publisher taxonomies, scored with wratio(), to a new csv
for p in pub_list:
       
    endnode = taxonomizer.GetTaxonomyNodes(p, 3, -1)

    best = ["NULL", "NULL"]
    score = 0

    for g in google_list:

        gnode = taxonomizer.GetTaxonomyNodes(g, 1, -1)

        if taxonomizer.CompareTaxonomyNodes(endnode, gnode, threshold):

            if fuzz.WRatio(endnode, gnode) > score:

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
        #rerun_.writerow(temp_list)
        temp.append(temp_list)
        miss_count += 1
        print "Misses 1st round: ", miss_count

miss_count = 0
rerun_list = []

for t in temp:

    best = ["NULL", "NULL"]
    score = 0

    for g in google_list:

        gnode = taxonomizer.GetTaxonomyNodes(g, 1, -1)

        # Try to grab second from end node
        try:
            endnode = taxonomizer.GetTaxonomyNodes(t, 3, -2)
        
        except IndexError:
            endnode_ = taxonomizer.GetTaxonomyNodes(t, 3, -1)

        if taxonomizer.CompareTaxonomyNodes(endnode, gnode, threshold):

            if fuzz.WRatio(endnode, gnode) > score:
            
                best = g
                score = fuzz.WRatio(endnode, gnode) > score

        clientid = t[0]
        name = t[1]
        taxonomyid = t[2]
        taxonomytext = t[3]

    if score > threshold:
        matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "2nd From End"]
        final_.writerow(matches)
        match_count += 1
        print match_count, " matches so far"
        print "Match in the second round! ", matches
    else:
        temp_list = [clientid, name, taxonomyid, taxonomytext, "NULL", "NULL", "Far"]
        rerun_list.append(temp_list)
        miss_count += 1
        print "Misses 2nd round: ", miss_count

miss_count = 0
temp = []

for r in rerun_list:
        
    best = ["NULL", "NULL"]
    score = 0

    # try to grab third from end node
    try:
        endnode = taxonomizer.GetTaxonomyNodes(t, 3, -3) 
    
    except IndexError:
        endnode = taxonomizer.GetTaxonomyNodes(t, 3, -1)
        
    for g in google_list:

        gnode = taxonomizer.GetTaxonomyNodes(g, 1, -1)

        if taxonomizer.CompareTaxonomyNodes(endnode, gnode, threshold):

            if fuzz.WRatio(endnode, gnode) > score:

                best = g
                score = fuzz.WRatio(endnode, gnode) > score   

        clientid = r[0]
        name = r[1]
        taxonomyid = r[2]
        taxonomytext = r[3]

    if score > threshold:
        matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "3rd From End"]
        final_.writerow(matches)
        match_count += 1
        print match_count, " matches so far"
        print "Match in the third round! ", matches
    else:
        temp_list = [clientid, name, taxonomyid, taxonomytext, "NULL", "NULL", "Far"]
        temp.append(temp_list)
        miss_count += 1
        print "Misses 3rd round: ", miss_count

miss_count = 0
bucket = []

for t in temp:

    best = ["NULL", "NULL"]
    score = 0    

    for g in google_list:

        t_ = taxonomizer.GetUniqueTaxonomyWords(t[3])
        g_ = taxonomizer.GetUniqueTaxonomyWords(g[1])

        if taxonomizer.CompareTaxonomyTokens(t_, g_, ratio_threshold):

            if fuzz.token_set_ratio(t_, g_) > score:

                best = g
                score = fuzz.token_set_ratio(t_, g_)

        clientid = t[0]
        name = t[1]
        taxonomyid = t[2]
        taxonomytext = t[3]

    if score > ratio_threshold:
        matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Token"]
        final_.writerow(matches)
        match_count += 1
        print match_count, " matches so far"
        print "Match in the token round! ", matches
    else:
        temp_list = [clientid, name, taxonomyid, taxonomytext, "NULL", "NULL", "Far"]
        bucket.append(temp_list)
        miss_count += 1
        print "Misses token round: ", miss_count

miss_count = 0

for b in bucket:

    best = ["NULL", "NULL"]
    score = 0    

    for g in google_list:

        b_ = taxonomizer.GetUniqueTaxonomyWords(t[3])
        g_ = taxonomizer.GetUniqueTaxonomyWords(g[1])

        sales = [
            "sale", "special", "deal", "promo", "offer", "save", "savings", "new arrival", "featured", "reduced", "refurbished", "free shipping", "exclusive", "online only", "value", "clearance", "top", "best seller", "open box", "price drop", "trade in", "door buster", "liquidation", "bundle", "campaign", "upgrade", "coupon", "trade in", 
        ]

        services = [
            "service", "installation", "repair", "warranty", "guarantee", "rewards", "replacement", "refund", "protection", "plan", "solutions", "customer service", "support", "delivery", "pickup", "setup", "financing", "layaway", "credit", "credit card", "photo center", "preorder"
        ]

        vintages = [
            "collectible",
            "antique",
            "vintage"
        ]


        for sale in sales:
            if sale in b_:
                best = ["-11", "Unmapped SKUs|All|Sales/Specials/Deals"]
                break

        for service in services:
            if service in b_:
                best = ["-13", "Unmapped SKUs|All|Warranties/Service"]
                break

        for vint in vintages:
            if vint in b_:
                best = ["150477", "Arts & Entertainment|Hobbies & Creative Arts|Collectibles"]

        if "brand" in b_:
            best = ["-14", "Unmapped SKUs|All|Brand Pages"]
            break


        clientid = b[0]
        name = b[1]
        taxonomyid = b[2]
        taxonomytext = b[3]

    if score > ratio_threshold:
        matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Bucket"]
        final_.writerow(matches)
        match_count += 1
        print match_count, " matches so far"
        print "Match in the last round! ", matches
    else:
        temp_list = [clientid, name, taxonomyid, taxonomytext, "NULL", "NULL", "Far"]
        rerun_.writerow(temp_list)
        miss_count += 1
        print "Misses bucket round: ", miss_count

final.close()
