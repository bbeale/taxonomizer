#!/usr/bin/env python
# -*- coding: utf-8 -*-
from taxonomizer import Taxonomizer
import os


def main():

    # filename
    fname = "FNAC 2"

    #index = -2

    # set file path names
    desktop = os.path.relpath("data")

    taxo = Taxonomizer()
    mappings = None
    countsheet = None
    temp = []

    with open(desktop + fname + ".csv", "r") as m:
        global mappings
        mappings = m.readlines()

    with open(desktop + "taxonomy_outputs/" + fname + " - Word Count.csv", "w") as c:
        global countsheet

        toprow = ["word", "count"]

        countsheet.writerow(toprow)

        for m in mappings:
            pt = taxo.get_unique_taxonomy_words(m[3])
            pt_ = m[3].split("|")
            print("pt_: ", pt_)
            for item in pt_:
                temp.append(item)

        counter, limit = taxo.get_most_frequent_word(temp)

        for key, value in counter.items():
            print("The word ", key, " occurred ", value, " times.")
            countsheet.writerow([key, value])

        countsheet.writerow(["Most frequent word: ", max])


if __name__ == "__main__":
    main()
