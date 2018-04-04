#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt

y = [x.strip().split(' ')[0] for x in sys.stdin.readlines()]
y_f = []
for ind, elem in enumerate(y):
    try:
        y_f.append(float(elem))
    except Exception as e:
        print('Bad value: {}'.format(elem))
y = y_f
x = [i for i in range(len(y))]


plt.plot(x, y, color='red', label='loss', linewidth='2')

plt.xlim([x[0], x[-1]])  
plt.ylim([0, max(y)])  
plt.xlabel(u'batch')  
plt.ylabel(u'loss')  
plt.title(u'loss')  
plt.legend(loc="upper right")  
plt.grid()
plt.show()  
