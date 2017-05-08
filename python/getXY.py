#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Xlib import display
data = display.Display().screen().root.query_pointer()._data
print data["root_x"], data["root_y"]
