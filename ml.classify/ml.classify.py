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
#%option
#%  key: hdf
#%  type: string
#%  description: Name of the HDF file, where al the results and stats will be saved
#%  required: yes
#%  answer: results.hdf
#%end
#%option
#%  key: data
#%  type: string
#%  description: Name of the statistic data contained in the HDF file
#%  required: yes
#%  answer: data
#%end
#%option
#%  key: training_json
#%  type: string
#%  description: Name of the JSON file with the name, cat, and a list of ids
#%  required: no
#%  guisection: Training
#%  answer: training.json
#%end
#%option
#%  key: training_kchk
#%  type: string
#%  description: Name for the training values in the HDF
#%  required: no
#%  answer:
#%  guisection: Training
#%end
#%option
#%  key: training_ychk
#%  type: string
#%  description: Name for the training values in the HDF
#%  required: no
#%  answer:
#%  guisection: Training
#%end
#%option
#%  key: training_number
#%  type: integer
#%  description: Number of training sample to use per category, if 0 all will be use
#%  required: no
#%  answer: 0
#%  guisection: Training
#%end
#%option
#%  key: training_conf
#%  type: string
#%  description: Name for the training configure file
#%  required: no
#%  answer:
#%  guisection: Training
#%end
#%option
#%  key: training_mls
#%  type: string
#%  description: Name of the dictionary containing the instance of the Machine Learning
#%  required: no
#%  answer: MLS
#%  guisection: Training
#%end
#%option
#%  key: training_key
#%  type: string
#%  description: Name of the key of the instance to train and use for classification
#%  required: no
#%  guisection: Training
#%end
#%option
#%  key: training_hdf
#%  type: string
#%  description: Name for the training HDF file, if not set the HDF with results will be used
#%  required: no
#%  answer:
#%  guisection: Training
#%end
#%option
#%  key: out_class
#%  type: string
#%  description: Name of the label in the HDF, to save the classification results
#%  required: no
#%  answer: %s
#%end
#%option
#%  key: transform
#%  type: string
#%  options: nothing,standardize,normalize
#%  description: Choose the traformation function of the statistics data of the segments
#%  required: no
#%  answer: nothing
#%end
#%option
#%  key: area_size
#%  type: integer
#%  description: Use only areas greater then N pixels
#%  required: no
#%  answer: 0
#%end

from __future__ import absolute_import, division, print_function, unicode_literals
import json
import sys
import imp

try:
    import pandas as pnd
except ImportError, e:
    print("""This module require Pandas to run.

Please install pandas: http://pandas.pydata.org/

""")
    raise ImportError(e)

from grass.script import parser
from grass.pygrass.functions import get_lib_path

path = get_lib_path("ml.class", "libmlcls")
if path is None:
    raise ImportError("Not able to find the path to libmlcls directory.")

sys.path.append(path)
from mlchk import check_classification
from mltraining import extract_itr, extract_training
from mltransform import transform
from mlclassify import mls_classification


def main(opts, flgs):
    if not opts['training_hdf']:
        opts['training_hdf'] = opts['hdf']

    df = pnd.read_hdf(opts['hdf'], str(opts['data']))
    data = df[df['non_null_cells'] > int(opts['area_size'])]
    if opts['training_kchk'] and opts['training_ychk']:
        Kchk = pnd.read_hdf(opts['training_hdf'], str(opts['training_kchk']))
        ychk = pnd.read_hdf(opts['training_hdf'], str(opts['training_ychk']))
        itr = extract_itr(Kchk, ychk, int(opts['training_number']))
    else:
        with open(opts['training_json'], 'r') as fp:
            tr = json.load(fp)
            check_classification(tr)
            itr, Kchk, ychk = extract_training(tr, data,
                                               int(opts['training_number']))

    conf = imp.load_source("conf", opts['training_conf'])
    mls = getattr(conf, opts['training_mls'])
    key = None if opts['training_key'] == '' else opts['training_key']

    tdata, tKchk = transform(opts['transform'], data, Kchk)
    tK_chk, y_chk = tKchk.loc[itr], ychk.loc[itr]

    mls_classification(tdata, tK_chk, y_chk, mls,
                       hdf=opts['hdf'], out_class=opts['out_class'],
                       key=key)


if __name__ == "__main__":
    options, flags = parser()
    main(options, flags)

"""
ml.classify training_json=training.json \
training_conf=mlconf.py \
training_mls=BEST \
training_hdf=/home/pietro/docdat/phd/edinburgh/segSVM/segments-ml/data.hdf \
training_kchk=K_chk \
training_ychk=y_chk \
hdf=results.hdf

"""
