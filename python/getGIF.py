#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands

print "Please select a window..."
results = commands.getoutput('xwininfo').split('\n')
x = eval(results[7].split(" ")[-1])
y = eval(results[8].split(" ")[-1])
w = eval(results[11].split(" ")[-1])
h = eval(results[12].split(" ")[-1])
print "window info", w,"x",h,"+",x,"+",y

import sys
length_s = 60
if len(sys.argv) == 2:
    length_s = eval(sys.argv[1])

commands.getoutput('byzanz-record -d {} -x {} -y {} -w {} -h {} output.gif'.format(length_s, x, y, w, h))
print "Saved in output.gif"
