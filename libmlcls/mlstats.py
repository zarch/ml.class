# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:14:59 2013

@author: pietro
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from subprocess import PIPE
from itertools import combinations

try:
    import pandas as pnd
except ImportError, e:
    print("""This module require Pandas to run.

Please install pandas: http://pandas.pydata.org/

""")
    raise ImportError(e)

from grass.pygrass.modules import Module


def get_gmaps(group):
    igrp = Module('i.group', flags='gl', group=group, stdout_=PIPE)
    return [str(g.split('@')[0]) for g in igrp.outputs.stdout.split()]


def cmpt_stats(segs, gmaps, statname=''):
    for gm in gmaps:
        Module('r.univar', flags='t', map=gm, zones=segs,
               output=statname % gm, separator=',', overwrite=True)


def get_pnl(gmaps, statname=''):
    dfs = {}
    for gm in gmaps:
        print("reading: ", statname % gm)
        dfs[gm] = pnd.read_csv(statname % gm, delimiter=',',
                               header=0, index_col='zone',
                               usecols=('zone', 'non_null_cells', 'min', 'max',
                                        'range', 'mean', 'stddev', 'varaiance',
                                        'coeff_var'))
    return pnd.Panel(dfs)


def pnl2df(pnl):
    x = pnl.keys()[0]
    df = pnd.DataFrame(index=pnl[x].index)
    df['non_null_cells'] = pnl[x]['non_null_cells']
    for key in pnl.keys():
        for col in pnl[key].keys():
            if col != 'non_null_cells':
                df["%s_%s" % (key, col)] = pnl[key][col]
    return df


def add_ratio(df, cols):
    for a, b in combinations(cols, 2):
        df['%s/%s' % (a, b)] = df[a]/df[b]


def statistics(group, zones, ratio, hdf, stat_name, stat_results):
    """r.univar(map='photo_b' zones='ortho_segs_l005'
                output='univarstats_b.csv' separator=',',
                overwrite=True, flags='t')"""
    gmaps = get_gmaps(group)
    cmpt_stats(zones, gmaps, stat_name)
    df = pnl2df(get_pnl(gmaps, stat_name))
    # 'photo_r_mean', 'photo_g_mean', 'photo_b_mean'
    add_ratio(df, ratio)
    df.to_hdf(hdf, str(stat_results))
    return df
