from fuzzywuzzy import fuzz
from Levenshtein import *
import datetime
import csv
import re

def CompareTaxonomyNodes(p, g, threshold):
    score = fuzz.WRatio(p, g)
    if score >= threshold:
        return True

def CompareTaxonomyTokens(p, g, threshold):
    score = fuzz.partial_token_sort_ratio(p, g)
    #score = fuzz.partial_token_set_ratio(p, g)
    if score >= threshold:
        return True

def SetReviewLevel(score):
    if score >= 95: return "Exact"
    elif score >= 90: return "Near"
    else: return "Far"

def AddFileContentsToList(filename):
    f = open(filename, "r")
    f_reader = csv.reader(f, delimiter=",", lineterminator="\n")
    f_list = []
    for fr in f_reader: f_list.append(fr)
    f.close()
    return f_list

def GetUniqueTaxonomyWords(tax):
    tax_ = re.sub("[^a-zA-Z]+", " ", tax)
    tax_ = tax_.split()
    tax_.sort()
    ulist = []
    [ulist.append(x) for x in tax_ if x not in ulist]
    ulist_ = " ".join(ulist)
    return ulist_

def GetTaxonomyWordsWithSymbols(tax):
    tax_ = re.sub("[^a-zA-Z%$]+", " ", tax)
    tax_ = tax_.split()
    tax_.sort()
    ulist = []
    [ulist.append(x) for x in tax_ if x not in ulist]
    ulist_ = " ".join(ulist)
    return ulist_

def GetTaxonomyNodes(taxonomy, selector, index): 
    # adjust index for pub or goog 
    taxonomy_list = taxonomy[selector].split("|")
    try:
        return taxonomy_list[index].strip().lower()
    except IndexError:
        return taxonomy_list[-1].strip().lower()

def GetMostFrequentWord(source):
    word_counter = {}
    for s in source:
        if word_counter.has_key(s):
            word_counter[s] += 1

        else:
            word_counter[s] = 1

    return (word_counter, max(word_counter, key=lambda key: word_counter[key]))

def CompareTaxonomies(pub, goog, index, threshold):

    list_of_matches = []
    list_to_rerun = []

    for p in pub:

        node_to_compare = GetTaxonomyNodes(p, 3, index)

        best = ["NULL", "NULL"]
        score = 0

        for g in goog:

            google_end_node = GetTaxonomyNodes(g, 1, -1)

            if CompareTaxonomyNodes(node_to_compare, google_end_node, threshold):

                if fuzz.WRatio(node_to_compare, google_end_node) > score:

                    best = g
                    score = fuzz.WRatio(node_to_compare, google_end_node)

            clientid = p[0]
            name = p[1]
            taxonomyid = p[2]
            taxonomytext = p[3]

            flag = SetReviewLevel(score)

        if score > threshold:
            matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], flag]
            list_of_matches.append(matches)
        else:
            temp_list = [clientid, name, taxonomyid, taxonomytext, "NULL", "NULL", "Far"]
            list_to_rerun.append(temp_list)
        
    return list_of_matches, list_to_rerun

def CompareTaxonomiesUsingTokens(pub, goog, index, threshold):
    
    list_of_matches = []
    list_to_rerun = []

    for p in pub:

        try:
            node_to_compare = GetUniqueTaxonomyWords(GetTaxonomyNodes(p, 3, index))
        except IndexError:
            node_to_compare = GetUniqueTaxonomyWords(GetTaxonomyNodes(p, 3, -1))
            
        best = ["NULL", "NULL"]
        score = 0    

        print "Comparing", node_to_compare            

        for g in goog:

            #google_node = GetTaxonomyNodes(g, 1, -1)
            google_node = GetUniqueTaxonomyWords(g[1])

            if CompareTaxonomyTokens(node_to_compare, google_node, threshold):

                if fuzz.partial_token_sort_ratio(node_to_compare, google_node) > score:
                #if fuzz.partial_token_set_ratio(node_to_compare, google_node) > score:

                    best = g
                    score = fuzz.partial_token_sort_ratio(node_to_compare, google_node)
                    #score = fuzz.partial_token_set_ratio(node_to_compare, google_node)

            clientid = p[0]
            name = p[1]
            taxonomyid = p[2]
            taxonomytext = p[3]

        if score > threshold:
            matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Token"]
            list_of_matches.append(matches)

        else:
            temp_list = [clientid, name, taxonomyid, taxonomytext, "NULL", "NULL", "Far"]
            list_to_rerun.append(temp_list)
        
    return list_of_matches, list_to_rerun

def MapBucketTaxonomies(pub):

    bucket = [
        "sale", "special", "deal", "promo", "offer", "save", "savings", "new arrival", "featured", "reduced", "refurbished", "free shipping", "event", "dollar", "online only", "value", "clearance", "best seller", "open box", "price drop", "trade in", "door buster", "liquidation", "bundle", "campaign", "upgrade", "coupon", "trade in", "service", "installation", "repair", "warranty", "guarantee", "rewards", "replacement", "refund", "customer", "delivery", "pickup", "setup", "financing", "layaway", "credit", "credit card", "photo center", "preorder", "$", "%", "test", "brand"
    ]

    list_of_matches = []
    
    for p in pub:  

        clientid = p[0]
        name = p[1]
        taxonomyid = p[2]
        taxonomytext = p[3].lower()
        best = ["NULL", "NULL"]

        for b in bucket:
            if IsInBucket(b, taxonomytext):
                print b, " is in ", taxonomytext
                best = ["-10", "Unmapped SKUs|All|Misc. Uncategorized"]
                

        matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Bucket"]
        list_of_matches.append(matches)

    return list_of_matches 

def IsInBucket(item, taxonomy):
    if item in taxonomy: 
        return True
    else:
        return False

def MapVintageTaxonomies(pub):

    vintages = [
        "collectible",
        "antique",
        "vintage"
    ]

    list_of_matches = []
    
    for p in pub:  

        clientid = p[0]
        name = p[1]
        taxonomyid = p[2]
        taxonomytext = p[3].lower()
        best = ["NULL", "NULL"]

        p_unique = GetUniqueTaxonomyWords(taxonomytext)
        p_unique = p_unique.lower()
        
        for vint in vintages:
            if IsInBucket(vint, taxonomytext):
                print vint, " is in ", taxonomytext
                best = ["150477", "Arts & Entertainment|Hobbies & Creative Arts|Collectibles"]

        matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Vintage"]
        list_of_matches.append(matches)

    return list_of_matches

def MapBooks(pub):

    list_of_matches = []
    
    for p in pub:  

        clientid = p[0]
        name = p[1]
        taxonomyid = p[2]
        taxonomytext = p[3].lower()
        best = ["NULL", "NULL"]

        p_unique = GetUniqueTaxonomyWords(taxonomytext)
        p_unique = p_unique.lower()
        
        if IsInBucket("book", taxonomytext):
            print "book is in ", taxonomytext
            best = ["153484", "Media|Books"]

        matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Book"]
        list_of_matches.append(matches)

    return list_of_matches

def MapGifts(pub):

    list_of_matches = []
    
    for p in pub:  

        clientid = p[0]
        name = p[1]
        taxonomyid = p[2]
        taxonomytext = p[3].lower()
        best = ["NULL", "NULL"]

        p_unique = GetUniqueTaxonomyWords(taxonomytext)
        p_unique = p_unique.lower()
        
        if IsInBucket("gift", taxonomytext):
            print "gift is in ", taxonomytext
            best = ["150790", "Arts & Entertainment|Party & Celebration|Gift Giving"]

        matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Gift"]
        list_of_matches.append(matches)

    return list_of_matches