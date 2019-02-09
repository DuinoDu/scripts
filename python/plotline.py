#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
cat log.txt | grep loss | cut -d ' ' -f 5 | cut -d ':' -f 1 | plotline.py
'''


import sys
import matplotlib.pyplot as plt

y = [x.strip().split(' ')[0] for x in sys.stdin.readlines()]
#y = [48.7, 50.0, 51.3, 53.6, 53.6, 54.0, 55.0, 55.1, 55.5]
y_f = []
for ind, elem in enumerate(y):
    try:
        y_f.append(float(elem))
    except Exception as e:
        print('Bad value: {}'.format(elem))
y = y_f
x = [i for i in range(len(y))]
#x = [22, 30, 40, 50, 60, 70, 80, 90, 100]


plt.plot(x, y, color='red', label='AP', linewidth=2)

plt.xlim([x[0], x[-1]])  
plt.ylim([min(y) - 5, max(y) + 5])  
plt.xlabel(u'epoch')  
plt.ylabel(u'AP')  
plt.title(u'AP-epoch')  
plt.legend(loc="lower right")  
plt.grid()
plt.show()  
