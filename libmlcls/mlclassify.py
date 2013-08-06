# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 14:14:28 2013

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


def classify(K_all, K_chk, y_chk, ml, save='', hdf=''):
    t0 = time.time()
    ml.learn(K_chk, y_chk)
    print("Time spent learning using %s: %.2fs" % (save, time.time() - t0))
    t0 = time.time()
    classified = ml.pred(K_all)
    print("Time spent classifing: %.2fs" % (time.time() - t0))
    ids = pnd.Series(data=classified, index=K_all.index)
    if save and hdf:
        print("Saving results as: %s in the hdf file" % save)
        ids.to_hdf(hdf, save)
    return ids


def mls_classification(K_all, K_chk, y_chk, mls, hdf, out_class):
    for k in mls:
        classify(K_all, K_chk, y_chk, mls[k], save=out_class % k, hdf=hdf)
