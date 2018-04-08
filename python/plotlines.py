#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np
import os


def str2float(input):
    output = []
    for e in input:
        try:
            output.append(float(e))
        except Exception as e:
            print('Bad value: {}'.format(e))
    return output


def align(Ys):
    minlen = len(Ys[0])
    maxY = 0 # may cause bug
    for y in Ys:
        if len(y) < minlen:
            minlen = len(y)
        if max(y) > maxY:
            maxY = max(y)
    Ys_align = []
    for y in Ys:
        Ys_align.append(y[:minlen])
    return Ys_align, maxY


def plot(args):
    Ys = []
    Zs = []
    names = []
    colors = ['red', 'green']
    linestyles = [':', '-']
    X = []
    if args.y1 != '':
        y = [x.strip() for x in open(args.y1, 'r').readlines()]
        y = str2float(y)
        Ys.append(y)
        names.append(os.path.basename(args.y1))

    if args.y2 != '':
        y = [x.strip() for x in open(args.y2, 'r').readlines()]
        y = str2float(y)
        Ys.append(y)
        names.append(os.path.basename(args.y2))

    if len(Ys) == 0:
        print('Empty input')
        return

    if args.z1 != '':
        z = [x.strip() for x in open(args.z1, 'r').readlines()]
        z = str2float(z)
        Zs.append(z)
        names.append(os.path.basename(args.z1))

    if args.z2 != '':
        z = [x.strip() for x in open(args.z2, 'r').readlines()]
        z = str2float(z)
        Zs.append(z)
        names.append(os.path.basename(args.z2))

    Ys, maxY = align(Ys)
    X = [i for i in range(len(Ys[0]))]

    fig, ax1 = plt.subplots()
    for ind, y in enumerate(Ys):
        ax1.plot(X, y, linestyle=linestyles[ind], color=colors[0], label=names[ind], linewidth=args.linewidth)
        ax1.set_xlabel(args.xlabel)
        ax1.set_xlim([X[0], X[-1]])  
        ax1.set_ylabel(u'loss')
        ax1.set_ylim([0, maxY])  
        for t in ax1.get_yticklabels():
            t.set_color(colors[0])

    if len(Zs) != 0:
        Zs, maxZ = align(Zs)
        X = [i * len(X)/len(Zs[0]) for i in range(1, 1+len(Zs[0]))]
        ax2 = ax1.twinx()
        for ind, z in enumerate(Zs):
            ax2.plot(X, z, linestyle=linestyles[ind], color=colors[1], label=names[ind+len(Ys)], linewidth=args.linewidth)
            ax2.set_ylabel(u'IU')
            ax2.set_ylim([0, 1.0])  
            for t in ax2.get_yticklabels():
                t.set_color(colors[1])
    
    plt.title(args.title)  
    plt.legend(loc="upper left")  
    plt.grid()
    plt.show()  


def main(args):
    plot(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot lines')
    parser.add_argument('--y1', default='', type=str, help='input y1 data, one data for one line')
    parser.add_argument('--y2', default='', type=str, help='input y2 data, one data for one line')
    parser.add_argument('--z1', default='', type=str, help='input z1 data, one data for one line')
    parser.add_argument('--z2', default='', type=str, help='input z2 data, one data for one line')
    parser.add_argument('--title', default='figure', type=str, help='plot title')
    parser.add_argument('--linewidth', default=3, type=int, help='line width')
    parser.add_argument('--xlabel', default='batch', type=str, help='xlabel')
    args = parser.parse_args()
    main(args)
