# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:45:53 2013

@author: pietro
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import time

from grass.pygrass.modules import Module


def get_seg_opts(s):
    dic = dict([[kv for kv in kv.strip().split('=')]
                for kv in s.strip().split(',')])
    for k in dic:
        if dic[k].isdigit():
            dic[k] = int(dic[k])
        else:
            try:
                dic[k] = float(dic[k])
            except ValueError:
                dic[k] = str(dic[k])
    return dic


def segment(thresholds, group,
            seg_opts='method=region_growing,similarity=euclidean,minsize=2',
            seg_name='seg__%.2f'):
    """
    * i.segment(group='rgb', output='ortho_segs_l002', threshold=0.02,
    method='region_growing', similarity='euclidean', minsize=1, iterations=20)
    * i.segment(group='rgb' output='ortho_segs_l005', threshold=0.05,
    method='region_growing', similarity='euclidean', minsize=2, iterations=20,
    seeds='ortho_segs_l002')
    """
    iseg = Module('i.segment')
    seg_opts = get_seg_opts(seg_opts)
    seg_opts['overwrite'] = True
    seeds = None
    for thr in thresholds:
        seg_opts['threshold'] = thr
        seg_opts['seeds'] = seeds
        seg_opts['group'] = group
        seg_opts['output'] = seg_name % thr
        st = time.time()
        iseg(**seg_opts)
        print("%s, required: %.2fs" % (seg_opts['output'], time.time() - st))
        seeds = seg_opts['output']  # update seeds
