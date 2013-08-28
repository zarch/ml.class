# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:44:30 2013

@author: pietro
"""


#
# TRANSFORMATION FUNCTIONS
#
def stdize(df, mean, std):
    return (df - mean) / std


def normalize(df, xmin, xmax):
    return (df - xmin) / (xmax - xmin)


def transform(method, data, chk):
    if method == 'standardize':
        mean, std = chk.mean(), chk.std()
        return stdize(data, mean, std), stdize(chk, mean, std)
    elif method == 'normalize':
        xmin, xmax = chk.min(), chk.max()
        return normalize(data, xmin, xmax), normalize(chk, xmin, xmax)
    elif method == 'nothing':
        return data, chk
    else:
        raise ValueError('method: <%s> not valid' % method)
