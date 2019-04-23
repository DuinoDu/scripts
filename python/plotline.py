#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
cat log.txt | grep loss | cut -d ' ' -f 5 | cut -d ':' -f 1 | plotline.py
'''


import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

y = [x.strip().split(' ')[0] for x in sys.stdin.readlines()]
y_f = []
for ind, elem in enumerate(y):
    try:
        y_f.append(float(elem)*100)
    except Exception as e:
        print('Bad value: {}'.format(elem))
y = y_f
x = [i+201 for i in range(len(y))]

_, ax = plt.subplots() 
ax.plot(x, y, color='red', label='lmks2lmk1pose-baseline', linewidth=2)

miny = min(y)
maxy = max(y)

ax.set_xlim([x[0], x[-1]])  
ax.set_ylim([miny, maxy])  
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_xlabel(u'epoch')  
ax.set_ylabel(u'err')  
ax.set_title(u'err-epoch')  
#ax.legend(loc="lower right")  
ax.grid()
plt.show()  
