#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
python checkgt.py jpeg_path [xml path]
'''
from __future__ import division
import os, sys
import os.path as osp
import cv2
import xml.etree.ElementTree as ET


def loadXML(xmlfile):
    tree = ET.parse(xmlfile)
    objs = tree.findall('object')
    boxes = []
    for ix, obj in enumerate(objs):
        bbox = obj.find('bndbox')
        # Make pixel indexes 0-based
        x1 = int(bbox.find('xmin').text) - 1
        y1 = int(bbox.find('ymin').text) - 1
        x2 = int(bbox.find('xmax').text) - 1
        y2 = int(bbox.find('ymax').text) - 1
        boxes.append([x1, y1, x2, y2])
    return boxes

def checkgt(argv):
    imgfile = osp.abspath(argv[1])
    xmlfile=''
    if len(argv) == 3:
        xmlfile = argv[2]
    else:
        dataset_root, img_name = os.path.split(imgfile)
        xml_name = osp.split( osp.splitext(imgfile)[0] )[1] + '.xml'
        xmlfile = osp.join(dataset_root, '..', 'Annotations', xml_name) 
    
    boxes = loadXML(xmlfile)
    img = cv2.imread(imgfile)

    factor = 1
    if img.shape[0] > 1000:
        factor = img.shape[0] / 1000
    img = cv2.resize(img, (int(img.shape[1]/factor), int(img.shape[0]/factor)))
    for box in boxes:
        box = [int(x/factor) for x in box]
        img = cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 255), 2)

    cv2.imshow('checkgt', img)
    cv2.waitKey(0)

def main():
    import sys
    if len(sys.argv) != 2:
        print(__doc__)
        return
    checkgt(sys.argv)

if __name__ == "__main__":
    main()
