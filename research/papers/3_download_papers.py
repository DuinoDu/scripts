#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import commands
import tqdm
import json

def merge(papers):
    papers_dict = dict()
    for p in papers:
        if p['url'] not in papers_dict.keys():
            papers_dict[p['url']] = p
        else:
            papers_dict[p['url']]['refered'] += p['refered']

    papers2 = []
    for k in papers_dict.keys():
        papers2.append(papers_dict[k])
    papers2 = sorted(papers2, key=lambda l : l["year"])
    return papers2


def download(args):
    papers = []
    if os.path.exists(args.json_file):
        with open(args.json_file, 'r') as fid:
            papers = json.load(fid)
    if 'url' not in papers[0].keys():
        print('You need to add url to each article in papers.json using fetch_papers.py')
        return
    papers = merge(papers)

    save_path = 'papers'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    lost = []
    t = tqdm.tqdm()
    t.total = len(papers)
    for cnt, p in enumerate(papers):
        t.update()
        print('downloading ', p['url'], '...')
        if len(str(p['url'])) == 0:
            lost.append(p['title'])
            continue
        try:
            p['title'] = str(p['title']).replace(' ', '_')
        except Exception as e:
            lost.append(p['title'])
            continue

        # download
        year = p['year']

        dst = "{}/{}_{}.pdf".format(save_path, p['year'], p['title'])
        cmd = 'wget -O {} {}'.format(dst, p['url'])
        try:
            (status, output) = commands.getstatusoutput(cmd)
        except Exception as e:
            lost.append(p['title'])
            continue
        output = output.split('\n')
        print('saved to ', dst)

    with open('lost_papers.txt', 'w') as fid:
        for l in lost:
            fid.write(l.encode('utf-8') + '\n')
    print('You need to download papers manually in lost_paper.txt')
    

def main(args):
    download(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dowload papers using papers.json')
    parser.add_argument('--json_file', default='papers.json', type=str, help='input json file')
    
    args = parser.parse_args()
    main(args)
