#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import json
import os
import time
import tqdm
import re

try:
    from selenium import webdriver
    b = webdriver.Chrome()
except Exception as e:
    print('Please install selenium and webdriver(Firefox or Chrome)')
    raise e


url = "https://scirate.com/arxiv/"

def get_bib(url):
    try:
        b.get(url)
        b.switch_to_window(b.current_window_handle)
    except Exception as e:
        return ""
    bibs = b.find_elements_by_class_name('bibtex')
    for bibarea in bibs:
        bibarea.click()
        bib = str(bibarea.text.encode('utf-8'))
        if len(bib) > 0:
            return bib
    return ""


def fetch_url(args):

    arxivID = lambda x : re.search('^[0-9]{4}\.[0-9]+', x)
    arxiv_pdfs = [x for x in os.listdir(args.input_dir) if arxivID(x) is not None]

    t = tqdm.tqdm()
    t.total = len(arxiv_pdfs)
    
    bibs = []
    for p in arxiv_pdfs:
        t.update()
        id = arxivID(p).group(0)
        bib = get_bib(url + id)
        bibs.append(bib)
        
    with open(args.output_file, 'w') as fid:
        for line in bibs:
            fid.write(line + '\n')

    print("Write to {}".format(args.output_file))


def main(args):
    fetch_url(args)
    b.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch bib from internet using arxiv ID')
    parser.add_argument('--input_dir', default='./', type=str, help='input directory')
    parser.add_argument('--output_file', default='ref.bib', type=str, help='output filename')
    args = parser.parse_args()
    main(args)
