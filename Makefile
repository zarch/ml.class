MODULE_TOPDIR = ../..

PGM=ml.class

SUBDIRS = \
        ml.segstats \
        ml.explore \
        ml.classify \
        ml.toraster \
        libmlcls

include $(MODULE_TOPDIR)/include/Make/Dir.make

default: parsubdirs htmldir

install: installsubdirs
