#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import argparse
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter

def readpdf(pdf_file, out_file='./pdf_out.txt'):
    #将一个pdf转换成txt
    def pdfTotxt(filepath,outpath):
        try:
            fp = file(filepath, 'rb')
            outfp=file(outpath,'w')

            #创建一个PDF资源管理器对象来存储共享资源
            rsrcmgr = PDFResourceManager(caching = False)

            # 创建一个PDF设备对象
            laparams = LAParams()
            laparams.all_texts = True
            device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=laparams,imagewriter=None)

            #创建一个PDF解析器对象
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for page in PDFPage.get_pages(fp, pagenos = set(),maxpages=0,
                                          password='',caching=False, check_extractable=True):
                page.rotate = page.rotate % 360
                interpreter.process_page(page)
                break
            #关闭输入流
            fp.close()
            #关闭输出流
            device.close()
            outfp.flush()
            outfp.close()
        except Exception, e:
             print("Exception:%s"%e)
    pdfTotxt(pdf_file, out_file)
   
def load_string(txt_file, split=['abstract', 'introduction']):
    start = split[0] 
    end = split[1] 
    with open(txt_file, 'r') as fid:
        contents = fid.readlines()  
        abstracts = []
        flag = False
        for ind, c in enumerate(contents):
            if start in c.lower():
                flag = True
                if start == '':
                    start = 'EOF'
            if flag:
                abstracts.append(c)
            if end in c.lower():
                flag = False

    # replace '-'
    new_abstract = ""
    for line in abstracts:
        line = line.strip('\n')
        if len(line) == 0:
            continue
        if '-' in line[-1]:
            line = line[:-1] 
        else:
            line += " "

        new_abstract += line
    abstracts = new_abstract
    abstracts = abstracts.strip(start)

    return abstracts

def test_spacy1(text_str):
    import spacy
    nlp = spacy.load('en')
    doc = nlp(text_str.decode('utf-8'))
    token = doc[0]
    print(token)

def main(args):
    txt_file = "pdf_out.txt"

    if not os.path.exists(txt_file):
        print("Parsing " + args.pdf + "...")
        readpdf(args.pdf, txt_file)
    else:
        print("{} exists. Read it.".format(txt_file))

    if args.title:
        title_str = load_string(txt_file, ['', 'abstract'])
        print('Title:')
        print(title_str)

    if args.abstract:
        abstract_str = load_string(txt_file, ['abstract', 'introduction'])
        print('Abstract:')
        print(abstract_str)

    #test_spacy1(abstract_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse arxiv paper')
    parser.add_argument('--pdf', default='', type=str, help='input pdf file')
    parser.add_argument('--title', default=1, type=int, help='print title')
    parser.add_argument('--abstract', default=1, type=int, help='print abstract')
    args = parser.parse_args()
    main(args)
