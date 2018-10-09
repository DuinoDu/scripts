#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
try:
    import commands
except Exception as e:
    import subprocess as commands


def run(cmd):
    print("run \"%s\"" % cmd)
    (status, output) = commands.getstatusoutput(cmd)
    return output


def main(args):
    ret = run('hadoop version')
    if 'not found' in ret:
        raise IOError, "hadoop not found"

    if not args.hdfs1.endswith('/'):
        args.hdfs1 += '/'
    if not args.hdfs2.endswith('/'):
        args.hdfs2 += '/'

    ret = run('hadoop fs -ls %s' % args.hdfs1).split('\n')
    files1 = [x.split(' ')[-1].split(args.hdfs1)[-1] for x in ret if 'hdfs' in x]

    ret = run('hadoop fs -ls %s' % args.hdfs2).split('\n')
    files2 = [x.split(' ')[-1].split(args.hdfs2)[-1] for x in ret if 'hdfs' in x]

    files_to_hdfs2 = [x for x in files1 if x not in files2]
    for f in files_to_hdfs2:
        run('hadoop fs -cp %s%s %s' % (args.hdfs1, f, args.hdfs2))

    if args.bi:
        files_to_hdfs1 = [x for x in files2 if x not in files1]
        for f in files_to_hdfs1:
            run('hadoop fs -cp %s%s %s' % (args.hdfs2, f, args.hdfs1))
    
    print('finish')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='rsync folders in two hdfs')
    parser.add_argument('--hdfs1', default='hdfs://hobot-bigdata/user/min.du/common/models/', type=str, help='first hdfs path')
    parser.add_argument('--hdfs2', default='hdfs://hobot-mosdata/user/min.du/common/models/', type=str, help='second hdfs path')
    parser.add_argument('--bi', dest='bi', action='store_true', help='bi direction')
    args = parser.parse_args()
    main(args)
