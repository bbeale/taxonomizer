#!/usr/bin/env python
# -*- coding: utf-8 -*-
from textwrap import dedent
import setuptools

setuptools.setup(
    name="taxonomizer",
    version="2.0",
    packages=["taxonomizer"],
    classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", ], license=dedent("""\
      Copyright (c) 2020 bbeale

      Permission is hereby granted, free of charge, to any person obtaining a copy
      of this software and associated documentation files (the "Software"), to deal
      in the Software without restriction, including without limitation the rights
      to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
      copies of the Software, and to permit persons to whom the Software is
      furnished to do so, subject to the following conditions:

      The above copyright notice and this permission notice shall be included in all
      copies or substantial portions of the Software.

      THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
      IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
      FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
      AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
      LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
      OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
      SOFTWARE."""), description="Python library for finding matches between distinctive sets of taxonomic classification",
    long_description=dedent("""\
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
      """),
    long_description_content_type="text/markdown",
    author="bbeale",
    author_email="beale.ben@gmail.com",
    url="https://github.com/bbeale/taxonomizer",
    setup_requires=["wheel", "setuptools"],
    install_requires=["urllib3", "requests", "fuzzywuzzy", "spacy"])
