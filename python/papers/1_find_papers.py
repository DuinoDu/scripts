#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import commands
import re
import json

keywords = ['context']

not_keywords = ['speech', 'sentense']

class Article(object):

    """One article in references"""

    def __init__(self, refer, cnt, pdf):
        self.text = self._revise(self._delete_head(refer))
        self.text_str = self._to_str(self.text)
        self.author = ""
        self.title = ""
        self.year = ""
        self.referedby = [pdf, cnt]
        
        self.parse_title()
        self.parse_year()
        self.parse_author()

    def _delete_head(self, list_str):
        for ind, l in enumerate(list_str):
            if ']' in l:
                return list_str[ind+2:]
        return list_str

    def _revise(self, input):
        output = []
        ind = 0
        while ind < len(input):
            if ind < len(input)-2 and input[ind+1] == '-' and input[ind+2] == '\n':
                output.append(input[ind] + input[ind+3])
                ind += 3
            elif input[ind] == '\n':
                output.append(' ')
                ind += 1
            else:
                output.append(input[ind])
                ind += 1
        return output

    def _to_str(self, list_str):
        s = ""
        for l in list_str:
            s += l
        return s

    def parse_title(self):
        for s in self.text_str.split('.'):
            if contains_keywords(s):
                self.title = s

    def parse_year(self):
        m = re.search('19[0-9]{2}|20[0-9]{2}', self.text_str)
        if m is not None:
            self.year = m.group(0)
        else:
            self.year = None
    
    def parse_author(self):
        pass

    def __str__(self):
        return self.text_str

def parse_pdf(pdf_file, txt_file):
    """Parse pdf using pdf2txt.py
    https://github.com/euske/pdfminer/

    Args:
        pdf_file (str): input pdf file
        txt_file (str): output txt file

    Returns:
        None
    """
    cmd = 'pdf2txt.py {} > {}'.format(pdf_file, txt_file)
    (status, output) = commands.getstatusoutput(cmd)
    output = output.split('\n')

def contains_keywords(s):
    s = s.lower()
    flag = False
    for k1 in keywords:
        if k1 in s and 'http' not in s:
            flag = True
            break
    for k2 in not_keywords:
        if k2 in s:
            flag = False
            break
    return flag

def get_reference(txt_file, args):
    """Find reference string in txt file.

    Args:
        txt_file (str): input txt file
        args () : None

    Returns:
        refers (list(str)): reference strings

    """
    pass

    refers = []
    refer = []

    def is_refer_head(s):
        if s.startswith('['):
            return True
        else:
            m = re.search('^[1-9]+\. ', s)
            if m is not None:
                return True
        return False


    with open(txt_file,'r') as fid:
        lines = [x.strip() for x in fid.readlines()]
        foundRefereces = False
        isRefer = False
        cnt = 0
        for line in lines:
            if line.startswith('References') or 'References' in line:
                foundRefereces = True
            if foundRefereces and is_refer_head(line):
                if len(refer) > 0:
                    cnt += 1
                    article = Article(refer, cnt, args.pdf)
                    if contains_keywords(article.text_str):
                        refers.append(article)
                    refer = []
                isRefer = True
            if isRefer: 
                refer += line
            if line == '\n':
                refer += line
                isRefer = False

        cnt += 1
        article = Article(refer, cnt, args.pdf)
        if contains_keywords(article.text_str):
            refers.append(article)

    return refers

def main(args):
    if args.pdf_dir != '':
        pdfs = sorted([os.path.join(args.pdf_dir, x) for x in sorted(os.listdir(args.pdf_dir)) if x.endswith('.pdf')])
    elif args.pdf != '':
        pdfs = [args.pdf]
    else:
        print('No input pdfs')
        return

    for pdf_file in pdfs:
        txt_file = "pdf_out.txt"
        if os.path.exists(txt_file) and not args.saving_cache:
            os.remove(txt_file)

        # parse pdf to txt
        parse_pdf(pdf_file, txt_file)

        # get references from txt 
        refers = get_reference(txt_file, args)

        year_title_list = []
        for r in refers:
            print(r.title)
            year_title_list.append({"year":r.year, "title":r.title, "refered":r.referedby})

        papers = []
        if os.path.exists(args.json_file):
            with open(args.json_file, 'r') as fid:
                papers = json.load(fid)

        papers += year_title_list
        papers = sorted(papers, key=lambda l : l["year"])

        with open(args.json_file, 'w') as fid:
            json.dump(papers, fid)

    if not args.saving_cache:
        os.remove(txt_file)

def str2bool(s):
    return s in  ['1', 'y', 't', 'true', 'yes']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search papers related to one topic according to Reference')
    parser.add_argument('--pdf', default='', type=str, help='input pdf')
    parser.add_argument('--pdf_dir', default='', type=str, help='input pdf folder')
    parser.add_argument('--json_file', default='papers.json', type=str, help='all papers titles stored in json')
    parser.add_argument('--saving_cache', default='n', type=str2bool, help='if saving cache')
    args = parser.parse_args()
    main(args)
