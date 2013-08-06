#!/usr/bin/env python
# -- coding: utf-8 --
#
############################################################################
#
# MODULE:	    ml.classify
#
# AUTHOR(S):   Pietro Zambelli (University of Trento)
#
# COPYRIGHT:	(C) 2013 by the GRASS Development Team
#
#		This program is free software under the GNU General Public
#		License (>=v2). Read the file COPYING that comes with GRASS
#		for details.
#
#############################################################################

#%Module
#%  description: Image fusion algorithms to sharpen multispectral with high-res panchromatic channels
#%  keywords: imagery
#%  keywords: machine learning
#%  keywords: classification
#%  overwrite: yes
#%End
#%option G_OPT_I_GROUP
#%  key: group
#%  description: Name of input imagery group
#%  required: yes
#%end
#%option
#%  key: hdf
#%  type: string
#%  description: Name of the HDF file, where al the results and stats will be saved
#%  required: yes
#%  answer: results.hdf
#%end
#%option
#%  key: seg_thresholds
#%  type: double
#%  multiple: yes
#%  description: Segment thresholds
#%  required: no
#%  answer: 0.01,0.02
#%end
#%option
#%  key: seg_opts
#%  type: string
#%  multiple: yes
#%  description: Segment options
#%  required: no
#%  answer: method=region_growing,similarity=euclidean,minsize=2
#%  guisection: Segment
#%end
#%option
#%  key: seg_name
#%  type: string
#%  description: Name for output raster maps from segment
#%  required: no
#%  answer: seg__%.2f
#%  guisection: Segment
#%end
#%option
#%  key: stat_name
#%  type: string
#%  description: Name for output raster maps from segment
#%  required: no
#%  answer: stat_%s.csv
#%  guisection: Statistics
#%end
#%option
#%  key: stat_ratio_cols
#%  type: string
#%  description: Columns name that you want to combine to compute the ratio
#%  required: no
#%  answer: photo_r_mean,photo_g_mean,photo_b_mean
#%  guisection: Statistics
#%end
#%option
#%  key: stat_results
#%  type: string
#%  description: Name for the statistics results in the HDF
#%  required: no
#%  answer: K_all
#%  guisection: Statistics
#%end
#%flag
#%  key: s
#%  description: Compute segment
#%end
#%flag
#%  key: r
#%  description: Compute statistics
#%end
from __future__ import absolute_import, division, print_function, unicode_literals
import sys

from grass.script import parser
from grass.pygrass.functions import get_lib_path


path = get_lib_path("ml.class", "libmlcls")
if path is None:
    raise ImportError("Not able to find the path to libmlcls directory.")

sys.path.append(path)
from mlstats import statistics
from mlsegment import segment


def main(opts, flgs):
    if 's' in flgs and flgs['s']:
        segment(opts['thrs'], opts['group'], opts['seg_opts'],
                opts['seg_name'])
    if 'r' in flgs and flgs['r']:
        statistics(opts['group'], opts['seg_name'] % opts['thrs'][-1],
                   opts['stat_ratio_cols'].split(','), opts['hdf'],
                   opts['stat_name'], opts['stat_results'])


if __name__ == "__main__":
    options, flags = parser()
    options['thrs'] = [float(thr)
                       for thr in options['seg_thresholds'].split(',')]
    main(options, flags)

"""
ml.classify group=rgb \
training_json=training.json \
training_conf=conf.py \
training_mls=BEST \
training_hdf=/home/pietro/docdat/phd/edinburgh/segSVM/segments-ml/data.hdf \
training_Kchk=K_chk \
training_ychk=y_chk -s -r -k -c


ml.segstats group=rgb hdf=results.hdf \
    seg_thresholds=0.01,0.02,0.05 \
    seg_opts="method=region_growing,similarity=euclidean,minsize=2" \
    seg_name=seg__%.2f \
    stat_name=stat_%s.csv \
    stat_ratio_cols=photo_r_mean,photo_g_mean,photo_b_mean \
    stat_results=K_all -s -r
"""
