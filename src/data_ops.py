from fuzzywuzzy import fuzz
from Levenshtein import *
import datetime
import csv
import re


class Taxonomizer:

    def __init__(self):
        pass

    def compare_nodes(self, p, g, threshold):
        return fuzz.WRatio(p, g) >= threshold

    def compare_tokens_sort(p, g, threshold):
        return fuzz.partial_token_sort_ratio(p, g) >= threshold

    def compare_tokens_set(p, g, threshold):
        return fuzz.partial_token_set_ratio(p, g) >= threshold

    def set_review_level(score):
        if score >= 95:
            result = "Exact"
        elif score >= 90:
            result = "Near"
        else:
            result = "Far"
        return result

    def add_file_contents_to_list(filename):
        with open(filename, "r") as f:
            f_reader = csv.reader(f, delimiter=",", lineterminator="\n")
            f_list = [fr for fr in f_reader]
        return f_list

    def get_unique_taxonomy_words(tax):
        newtax = re.sub("[^a-zA-Z]+", " ", tax).split()
        newtax.sort()
        ulist = []
        for node in newtax:
            if node not in ulist:
                ulist.append(node)
        return " ".join(ulist)

    def get_taxonomy_words_and_symbols(tax):
        newtax = re.sub("[^a-zA-Z%$]+", " ", tax).split()
        newtax.sort()
        ulist = []
        for node in newtax:
            if node not in ulist:
                ulist.append(node)
        return " ".join(ulist)


    def get_taxonomy_nodes(taxonomy, selector, index):
        # adjust index for pub or goog
        taxonomy_list = taxonomy[selector].split("|")
        results = []
        try:
            results = taxonomy_list[index].strip().lower()
        except IndexError:
            results = taxonomy_list[-1].strip().lower()
        finally:
            return results


    def get_most_frequent_word(source):
        word_counter = {}
        for s in source:
            if word_counter[s]:
                word_counter[s] += 1
            else:
                word_counter[s] = 1
        return word_counter, max(word_counter, key=lambda key: word_counter[key])


    def compare_taxonomies(pub, goog, index, threshold):

        clientid            = None
        name                = None
        taxonomyid          = None
        taxonomytext        = None
        flag                = None
        list_of_matches     = []
        list_to_rerun       = []

        for p in pub:

            node_to_compare = get_taxonomy_nodes(p, 3, index)
            best            = ["NULL", "NULL"]
            score           = 0

            for g in goog:
                google_end_node = get_taxonomy_nodes(g, 1, -1)
                if compare_nodes(node_to_compare, google_end_node, threshold):
                    if fuzz.WRatio(node_to_compare, google_end_node) > score:
                        best = g
                        score = fuzz.WRatio(node_to_compare, google_end_node)

                clientid        = p[0]
                name            = p[1]
                taxonomyid      = p[2]
                taxonomytext    = p[3]
                flag            = set_review_level(score)

            if score > threshold:
                matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], flag]
                list_of_matches.append(matches)
            else:
                temp_list = [clientid, name, taxonomyid, taxonomytext, "NULL", "NULL", "Far"]
                list_to_rerun.append(temp_list)
        return list_of_matches, list_to_rerun


    def compare_taxonomies_by_token(pub, goog, index, threshold):

        clientid            = None
        name                = None
        taxonomyid          = None
        taxonomytext        = None
        list_of_matches     = []
        list_to_rerun       = []

        for p in pub:
            try:
                node_to_compare = get_unique_taxonomy_words(get_taxonomy_nodes(p, 3, index))
            except IndexError:
                node_to_compare = get_unique_taxonomy_words(get_taxonomy_nodes(p, 3, -1))

            best    = ["NULL", "NULL"]
            score   = 0

            print("Comparing", node_to_compare)

            for g in goog:
                # google_node = get_taxonomy_nodes(g, 1, -1)
                google_node = get_unique_taxonomy_words(g[1])
                if compare_tokens_sort(node_to_compare, google_node, threshold):
                    if fuzz.partial_token_sort_ratio(node_to_compare, google_node) > score:
                    # if fuzz.partial_token_set_ratio(node_to_compare, google_node) > score:
                        best    = g
                        score   = fuzz.partial_token_sort_ratio(node_to_compare, google_node)
                        # score = fuzz.partial_token_set_ratio(node_to_compare, google_node)

                clientid        = p[0]
                name            = p[1]
                taxonomyid      = p[2]
                taxonomytext    = p[3]

            if score > threshold:
                matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Token"]
                list_of_matches.append(matches)
            else:
                temp_list = [clientid, name, taxonomyid, taxonomytext, "NULL", "NULL", "Far"]
                list_to_rerun.append(temp_list)
        return list_of_matches, list_to_rerun


    def map_bucket_taxonomies(pub):

        bucket = [
            "sale", "special", "deal", "promo", "offer", "save", "savings", "new arrival", "featured", "reduced", "refurbished", "free shipping", "event", "dollar", "online only", "value", "clearance", "best seller", "open box", "price drop", "trade in", "door buster", "liquidation", "bundle", "campaign", "upgrade", "coupon", "trade in", "service", "installation", "repair", "warranty", "guarantee", "rewards", "replacement", "refund", "customer", "delivery", "pickup", "setup", "financing", "layaway", "credit", "credit card", "photo center", "preorder", "$", "%", "test", "brand"
        ]

        list_of_matches = []

        for p in pub:

            clientid        = p[0]
            name            = p[1]
            taxonomyid      = p[2]
            taxonomytext    = p[3].lower()
            best            = ["NULL", "NULL"]

            for b in bucket:
                if is_in_bucket(b, taxonomytext):
                    print(b, " is in ", taxonomytext)
                    best = ["-10", "Unmapped SKUs|All|Misc. Uncategorized"]

            matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Bucket"]
            list_of_matches.append(matches)
        return list_of_matches


    def is_in_bucket(item, taxonomy):
        return item in taxonomy


    def map_vintage_taxonomies(pub):

        vintages = [
            "collectible",
            "antique",
            "vintage"
        ]

        list_of_matches = []

        for p in pub:

            clientid        = p[0]
            name            = p[1]
            taxonomyid      = p[2]
            taxonomytext    = p[3].lower()
            best            = ["NULL", "NULL"]

            p_unique = get_unique_taxonomy_words(taxonomytext)

            for vint in vintages:
                if is_in_bucket(vint, taxonomytext):
                    print(vint, " is in ", taxonomytext)
                    best = ["150477", "Arts & Entertainment|Hobbies & Creative Arts|Collectibles"]
            matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Vintage"]
            list_of_matches.append(matches)
        return list_of_matches


    def map_books(pub):

        list_of_matches = []

        for p in pub:

            clientid        = p[0]
            name            = p[1]
            taxonomyid      = p[2]
            taxonomytext    = p[3].lower()
            best            = ["NULL", "NULL"]

            p_unique = get_unique_taxonomy_words(taxonomytext)

            if is_in_bucket("book", taxonomytext):
                print("book is in ", taxonomytext)
                best = ["153484", "Media|Books"]
            matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Book"]
            list_of_matches.append(matches)
        return list_of_matches


    def map_gifts(pub):

        list_of_matches = []

        for p in pub:

            clientid        = p[0]
            name            = p[1]
            taxonomyid      = p[2]
            taxonomytext    = p[3].lower()
            best            = ["NULL", "NULL"]

            p_unique = get_unique_taxonomy_words(taxonomytext)

            if is_in_bucket("gift", taxonomytext):
                print("gift is in ", taxonomytext)
                best = ["150790", "Arts & Entertainment|Party & Celebration|Gift Giving"]
            matches = [clientid, name, taxonomyid, taxonomytext, best[0], best[1], "Gift"]
            list_of_matches.append(matches)
        return list_of_matches
