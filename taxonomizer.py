from dataops import taxonomizer
from fuzzywuzzy import fuzz
import csv




# Enter file namme
filename = "FNAC 2"
threshold = 88
index = -1




p_list = taxonomizer.AddFileContentsToList("c:\\Users\\bbeale\\Desktop\\" + filename + ".csv")
g_list = taxonomizer.AddFileContentsToList("includes\\googletaxonomy.csv")
# toprow for output file
toprow = ["ClientId", "Name", "PublisherTaxonomyId", "PublisherTaxonomyText", "GlobalTaxonomyId", "GlobalTaxonomyText", "Flag"]
# create output file, write top row
with open("c:\\Users\\bbeale\\Desktop\\taxonomy_outputs\\" + filename + " - MAPPED.csv", "w") as final:                       # change output filename
    final_ = csv.writer(final, delimiter=',', lineterminator='\n')
    final_.writerow(toprow)

final_list = []
rerun_list = []




## Call taxonomizer functions here :

# Normal node comparison :
final_list, rerun_list = taxonomizer.CompareTaxonomies(p_list, g_list, index, threshold)

# Catch bucket taxonomies :
#final_list = taxonomizer.map_bucket_taxonomies(p_list)

# Catch vintage / collectibles :
#final_list = taxonomizer.map_vintage_taxonomies(p_list)

# Catch books :
#final_list = taxonomizer.map_books(p_list)



# Catch partial token sorted ratios (good for when nodes contain matching strings and have unequal length)
#final_list, rerun_list = taxonomizer.compare_taxonomies_by_token(p_list, g_list, index, threshold)



# Write matches to final file and misses to rerun file
print "Final: ", type(final_list), len(final_list)

for fl in final_list:
    final = open("c:\\Users\\bbeale\\Desktop\\taxonomy_outputs\\" + filename + " - MAPPED.csv", "a")
    final_ = csv.writer(final, delimiter=',', lineterminator='\n')
    final_.writerow(fl)
    final.close()

for rl in rerun_list:
    rerun = open("c:\\Users\\bbeale\\Desktop\\taxonomy_outputs\\" + filename + " - RERUN.csv", "a")
    rerun_ = csv.writer(rerun, delimiter=',', lineterminator='\n')
    rerun_.writerow(rl)
    rerun.close()