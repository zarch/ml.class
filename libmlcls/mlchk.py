# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:42:34 2013

@author: pietro
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from itertools import combinations


def check_classification(diz):
    chk = dict()
    for key in diz:
        chk[key] = set(diz[key]['ids'])
        print("%s: %d" % (key, len(chk[key])))

    for k0, k1 in combinations(chk.keys(), 2):
        intersection = chk[k0] & chk[k1]
        if intersection:
            print("%s & %s have this segments in common: " % (k0, k1))
            for i in intersection:
                print("    %d" % i)
