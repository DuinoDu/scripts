#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import commands
import tqdm


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


def get_title(txt_file):
    if not os.path.exists(txt_file):
        return ""

    with open(txt_file,'r') as fid:
        lines = [x.strip() for x in fid.readlines()]
        if len(lines) != 0:
            return lines[0]
        else:
            return ""



def refine(args):
    pdfs = sorted([os.path.join(args.pdf_dir, x) for x in sorted(os.listdir(args.pdf_dir)) if x.endswith('.pdf')])

    txt_file = "pdf_out.txt"
    if os.path.exists(txt_file):
        os.remove(txt_file)

    t = tqdm.tqdm()
    t.total = len(pdfs)

    for pdf in pdfs:
        t.update()
        parse_pdf(pdf, txt_file)
        title = get_title(txt_file)
        if len(title) > 0:
            year = os.path.split(pdf)[1][:4]
            os.rename(pdf, os.path.join(args.pdf_dir, 
                                    "{}_{}.pdf".format(year, title.replace(' ', '_'))))
        if os.path.exists(txt_file):
            os.remove(txt_file)

def main(args):
    refine(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Refine title of papers')
    parser.add_argument('--pdf_dir', default='papers', type=str, help='paper pdf directory')
    
    args = parser.parse_args()
    main(args)
