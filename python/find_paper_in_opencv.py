#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import re
import fnmatch
import argparse

def iterfindfiles(path, fnexp):
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)

def getPaper(dir_path):
    # find bib files
    files = []
    for f in iterfindfiles(dir_path, "*.bib"):
        files.append(f)

    # read bib
    papers = [] #paper = {"title":"", "year":0}
    for f in files:
        with open(f, 'r') as fid:
            lines = fid.readlines()

        record = ["", 0]
        for line in lines:
            line = line.split('\n')[0]

            if 'title' in line and 'booktitle' not in line:
                result = re.findall(ur'(?<=[\{（])[^\)）]+(?=[\}）])', line.split('\n')[0])
                if len(result) != 0:
                    record[0] = result[0]
            elif 'year' in line:
                result = re.findall(ur'(?<=[\{（])[^\)）]+(?=[\}）])', line.split('\n')[0])
                if len(result) != 0:
                    record[1] = eval(re.findall('[0-9]+', result[0])[0])

            if record[0]!= "" and record[1] != 0:
                papers.append({"title":record[0], "year":record[1]})
                record = ["", 0]

            # only title
            if line == '}':
                if record[0] != "":
                    papers.append({"title":record[0], "year": 0})
                record = ["", 0]
    return papers 


def main(args):
    papers = getPaper(args.opencv_path)
    papers = sorted(papers, key=lambda paper : paper.values()[0])

    if not os.path.exists(args.out_file):
        with open(args.out_file, 'w') as fid:
            for p in papers:
                fid.write(str(p["year"]) + "    " + p["title"] + '\n')
    print("result saved in " + args.out_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find paper implemented in opencv')
    parser.add_argument('--path', default='opencv', type=str, help='opencv path')
    parser.add_argument('--out_file', default='paperlist.txt', type=str, help='output file name')
    args = parser.parse_args()
    main(args)
