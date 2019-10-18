#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import tqdm
import re
import commands


def download(index):
    cmd = 'arxiv download -t 60 ' + index
    (status, output) = commands.getstatusoutput(cmd)
    output = output.split('\n')

def main(args):
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    is_arxivID = lambda x : re.search('^[0-9]{4}\.[0-9]+', x) is not None
    arxiv_pdfs = [x for x in os.listdir(args.input) if is_arxivID(x)]

    t = tqdm.tqdm()
    t.total = len(arxiv_pdfs)

    for p in arxiv_pdfs:
        t.update()
        download(p[:-4])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch bib from internet using arxiv ID')
    parser.add_argument('--input', default='./', type=str, help='input directory')
    parser.add_argument('--output', default='output', type=str, help='description')
    args = parser.parse_args()
    main(args)
