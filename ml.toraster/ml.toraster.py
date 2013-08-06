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
#%  description: Export machine learning results to a raster map
#%  keywords: imagery
#%  keywords: machine learning
#%  keywords: classification
#%  overwrite: yes
#%End
#%option G_OPT_R_INPUT
#%  key: segment
#%  description: Name for the segment map
#%  required: yes
#%end
#%option
#%  key: hdf
#%  type: string
#%  description: Name of the HDF file, where al the results and stats are saved
#%  required: yes
#%  answer: results.hdf
#%end
#%option
#%  key: mlname
#%  type: string
#%  description: Name of the ML results
#%  required: yes
#%end
#%option G_OPT_R_OUTPUT
#%  key: output
#%  description: Name for the segment map
#%  required: yes
#%end
from __future__ import absolute_import, division, print_function, unicode_literals
import sys

from grass.script import parser
from grass.pygrass.functions import get_lib_path


path = get_lib_path("ml.class", "libmlcls")
if path is None:
    raise ImportError("Not able to find the path to libmlcls directory.")

sys.path.append(path)
from mlwriterast import ml2rast


def main(opts, flgs):
    ml2rast(opts['segment'], opts['output'],
            hdf=opts['hdf'], idsname=opts['mlname'])


if __name__ == "__main__":
    options, flags = parser()
    main(options, flags)
