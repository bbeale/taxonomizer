#taxonomizer

Given two lists of taxonomic classifications, for each item in the first list, find the closest matching element in
 the second list.
 
##Status as of Summer 2020

This project has not been actively used since 2016. It was hastily developed as a set of CLI utilities, intended for use on a local dev environment, built in parallel with the task that I was trying to automate. Despite these excuses and my self-deprecating attempts to laugh at them, the project nonetheless needs updating. 

Another project on my someday/maybe list has caused me to become interested in this project once again. The current core
 functionality has been refactored into a class and type hinting has been added. Future
 updates will completely overhaul the algorithm to make use of natural language processing.

##Roadmap

- Find a natural language processing technique that can accurately determine if two taxonomy strings are similar.
    - Topic model each taxonomy with child nodes weighted increasingly more heavily than parent nodes to give
     preference to taxonomies with more distinc, specific child nodes.
- Add unit tests.

##Setup

1. Clone the repository

`git clone https://github.com/bbeale/dataops [path/to/repo]`

2. Install the module

`python -m pip install path/to/repo`

3. Implement your comparison

```
from taxonomizer import Taxonomizer

taxo = Taxonomizer()

p_list = taxo.add_file_contents_to_list(outfilename)
g_list = taxo.add_file_contents_to_list(googfilename)

final_list, rerun_list = taxo.compare_taxonomies(p_list, g_list, index, threshold)
```

##Legacy Algorithm
Given a collection of strings representing a taxonomy node, match the end node to the best fitting node in a different collection of similar strings.

1. Start with a threshold in the mid to upper 90s (100 if it seems feasible based on pub taxonomies) and an index of -1
2. Repeat with the same index as necessary, lowering the threshold gradually no more than 90 (as the threshold drops < 90 the number of incorrect matches will skyrocket)
3. Run token match on the end nodes (need to raise threshold for this as there will be higher false matches)**
4. Repeat steps 1, 2 and 3 as necessary with decrementing indices (target the second from end publisher node, third from end, etc)
5. Use functions to map books/collectibles/bucket taxonomy items


** Token matches have proven to be the least consistent, but still have some relevance depending on the taxonomy structure
