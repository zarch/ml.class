# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 14:11:54 2013

@author: pietro
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import random as rnd
import numpy as np

try:
    import pandas as pnd
except ImportError, e:
    print("""This module require Pandas to run.

Please install pandas: http://pandas.pydata.org/

""")
    raise ImportError(e)


def extract_training(tran, df, n=None):
    res_data = []
    res_clas = []
    res_indx = []
    res_trn = []
    for key in tran.keys():
        for rid in tran[key]['ids']:
            res_data.append(df.loc[rid])
            res_clas.append(tran[key]['cat'])
            res_indx.append(rid)
        #import ipdb; ipdb.set_trace()
        rnd.shuffle(tran[key]['ids'])
        res_trn.extend(tran[key]['ids'][:n] if n else tran[key]['ids'])
    K_chk = pnd.Series(data=res_data, index=res_indx)
    y_chk = pnd.Series(data=res_clas, index=res_indx)
    itraining = pnd.Index(data=res_trn, dtype=np.int)
    return itraining, K_chk, y_chk


def extract_itr(Kchk, ychk, n=None):
    itr = []
    if n == 0:
        n = None
    for cat in set(ychk):
        itr.extend(ychk.index[ychk == cat][:n])
    return pnd.Index(data=itr, dtype=np.int)
