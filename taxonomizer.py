#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.data_ops import DataOps
import csv
import os


def main():
    """Initialize variables and run the algorithm

    :return:
    """
    filename = "FNAC 2"
    threshold = 88
    index = -1
    datadir = os.path.relpath("data")
    outputdir = os.path.relpath("output")

    do = DataOps()
    p_list = do.add_file_contents_to_list("{}/{}.csv".format(datadir, filename))
    g_list = do.add_file_contents_to_list("{}/googletaxonomy.csv".format(datadir))

    # toprow for output file
    toprow = ["ClientId", "Name", "PublisherTaxonomyId", "PublisherTaxonomyText", "GlobalTaxonomyId", "GlobalTaxonomyText", "Flag"]
    # create output file, write top row
    with open("{}/{}_MAPPED.csv".format(outputdir, filename), "w") as final:
        final_ = csv.writer(final, delimiter=',', lineterminator='\n')
        final_.writerow(toprow)

    # Normal node comparison
    final_list, rerun_list = do.compare_taxonomies(p_list, g_list, index, threshold)

    # Write matches to final file and misses to rerun file
    print("Final: ", type(final_list), len(final_list))

    for fl in final_list:
        with open("{}/{}_MAPPED.csv".format(outputdir, filename), "w") as final:
            final.write(fl)

    for rl in rerun_list:
        with open("{}/{}_MAPPED.csv".format(outputdir, filename), "w") as rerun:
            rerun.write(rl)


if __name__ == "__main__":
    main()
