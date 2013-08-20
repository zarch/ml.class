# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 12:18:29 2013

@author: pietro
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import time

try:
    import pandas as pnd
except ImportError, e:
    print("""This module require Pandas to run.

Please install pandas: http://pandas.pydata.org/

""")
    raise ImportError(e)

from grass.pygrass.raster import RasterRow


def ml2rast(segsname, outname, hdf=None, idsname=None, ids=None):
    ids = ids if ids else pnd.read_hdf(hdf, idsname)
    t0 = time.time()
    segs = RasterRow(segsname)
    segs.open('r')
    out = RasterRow(outname)
    out.open('w', mtype='CELL', overwrite=True)
    for row in segs:
        for i, col in enumerate(row):
            try:
                row[i] = ids[col]
            except KeyError:
                row[i] = 0
        out.put_row(row)
    segs.close()
    out.close()
    print("Time spent writing the raster %s: %.2fs" % (outname,
                                                       time.time() - t0))