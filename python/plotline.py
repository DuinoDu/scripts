#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
cat log.txt | grep loss | cut -d ' ' -f 5 | cut -d ':' -f 1 | plotline.py
'''


import sys
import matplotlib.pyplot as plt

y = [x.strip().split(' ')[0] for x in sys.stdin.readlines()]
y_f = []
for ind, elem in enumerate(y):
    try:
        y_f.append(float(elem)*100)
    except Exception as e:
        print('Bad value: {}'.format(elem))
y = y_f
x = [i*10 for i in range(len(y))]


plt.plot(x, y, color='red', label='lmks2lmk1pose-baseline', linewidth=2)

plt.xlim([x[0], x[-1]])  
plt.ylim([0, max(y)+1])  
plt.xlabel(u'epoch')  
plt.ylabel(u'err')  
plt.title(u'err-epoch')  
plt.legend(loc="lower right")  
plt.grid()
plt.show()  
