#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
################
Tool Description

Usage:
python main.py title.pdf
or
readpdf title.pdf
################
'''

import os
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
             print "Exception:%s",e
    pdfTotxt(pdf_file, out_file)
   
def load_abstract(txt_file):
    start = "abstract"
    end = "introduction"
    with open(txt_file, 'r') as fid:
        contents = fid.readlines()  
        abstracts = []
        flag = False
        for c in contents:
            if start in c.lower():
                flag = True
            if end in c.lower():
                flag = False
            if flag:
                abstracts.append(c)

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

def main(argv):
    pdf_file = argv[1]
    txt_file = "pdf_out.txt"

    if not os.path.exists(txt_file):
        print "Parsing ", pdf_file, "..."
        readpdf(pdf_file, txt_file)
    else:
        print "{} exists. Read it.".format(txt_file)

    abstract_str = load_abstract(txt_file)
    print abstract_str

    #test_spacy1(abstract_str)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(__doc__)
    else:
        main(sys.argv)

