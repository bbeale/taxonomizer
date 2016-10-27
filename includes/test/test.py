from dataops import taxonomizer
from fuzzywuzzy import fuzz
from Levenshtein import *
import datetime, csv
import jellyfish


p = ["308", "Shoptime", "3165364", "books|law|international law international law law law law"]
g = "playsets"

#rint fuzz.partial_token_sort_ratio(p, g)
#print fuzz.partial_ratio(p, g)




# Enter file namme
filename = "TescoDirect4 - RERUN"
threshold = 90
index = -1


print taxonomizer.GetUniqueTaxonomyWords(taxonomizer.GetTaxonomyNodes(p,3, -1))




#res = fuzz._token_sort(p, g)
#res_ = fuzz.partial_ratio(p, g)
#res__ = fuzz.ratio(p, g)
#res___ = fuzz._token_set(p, g)
#print res

