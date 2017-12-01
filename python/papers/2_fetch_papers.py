#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import json
import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import tqdm

from selenium import webdriver
b = webdriver.Chrome()
url = "https://cn.bing.com/search?q={}&ensearch=1"


def get_pdf_url(url):
    try:
        b.get(url)
    except Exception as e:
        return ""
    time.sleep(1)
    searchboxes = b.find_elements_by_class_name('b_algo')
    for box in searchboxes:
        link = str(box.find_element_by_tag_name('a').get_attribute('href'))
        if link.endswith('.pdf'):
            return link
    return ""


def fetch_url(args):

    papers = []
    if os.path.exists(args.json_file):
        with open(args.json_file, 'r') as fid:
            papers = json.load(fid)

    t = tqdm.tqdm()
    t.total = len(papers)
            
    new_papers = []
    for p in papers:
        t.update()
        title = p["title"].replace(' ', '+')
        title += "+pdf"
        try:
            p["url"] = get_pdf_url(url.format(title))
        except Exception as e:
            p["url"] = ""
        new_papers.append(p)
        
    with open(args.json_file, 'w') as fid:
        json.dump(new_papers, fid)
    print("Write to {}".format(args.json_file))


def main(args):
    fetch_url(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch urls from internet using papers.json')
    parser.add_argument('--json_file', default='papers.json', type=str, help='input json file')
    args = parser.parse_args()
    main(args)
