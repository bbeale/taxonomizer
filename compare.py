def CompareTaxonomies(st, ls):
    st_ = st[2].split("|")
    endnode = st_[-1].rstrip().lower()
    matches = []
    for item in ls:
        item_ = item[1].split("|")
        gnode = item_[-1].rstrip().lower()

        score = fuzz.wratio(endnode, gnode)

        if score > 70:
            result = [score, st, item]
            matches.append(result)
        elif score > 50
            result = [score, st, item]
            matches.append(result)
    matches.sort()
    return matches[0]

