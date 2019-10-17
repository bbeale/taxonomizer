Given a collection of strings representing a taxonomy node, match the end node to the best fitting node in a different collection of similar strings.

1. Start with a threshold in the mid to upper 90s (100 if it seems feasible based on pub taxonomies) and an index of -1
2. Repeat with the same index as necessary, lowering the threshold gradually no more than 90 (as the threshold drops < 90 the number of incorrect matches will skyrocket)
3. Run token match on the end nodes (need to raise threshold for this as there will be higher false matches)**
4. Repeat steps 1, 2 and 3 as necessary with decrementing indices (target the second from end publisher node, third from end, etc)
5. Use functions to map books/collectibles/bucket taxonomy items


** Token matches have proven to be the least consistent, but still have some relevance depending on the taxonomy structure


This is pretty much a dead project that I have no immediate plans to use again, outside of messing around with spaCy, but you never know when use cases for old code will present themselves. 