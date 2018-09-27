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

    ret1 = run('hadoop fs ls %s' % args.hdfs1).split('\n')
    for l in ret1:
        print(l)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='rsync folders in two hdfs')
    parser.add_argument('--hdfs1', default='hdfs://hobot-bigdata/user/min.du/common/models', type=str, help='first hdfs path')
    parser.add_argument('--hdfs2', default='hdfs://hobot-mosdata/user/min.du/common/models', type=str, help='second hdfs path')
    args = parser.parse_args()
    main(args)
