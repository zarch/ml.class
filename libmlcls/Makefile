MODULE_TOPDIR = ../../..

include $(MODULE_TOPDIR)/include/Make/Other.make
include $(MODULE_TOPDIR)/include/Make/Python.make

MODULES = mlchk mlclassify mlconf mlplts mlsegment mlstats mltraining \
          mlwriterast mltransform

ETCDIR = $(ETC)/ml.class

PYFILES := $(patsubst %,$(ETCDIR)/%.py,$(MODULES))
PYCFILES := $(patsubst %,$(ETCDIR)/%.pyc,$(MODULES))

default: $(PYFILES) $(PYCFILES)

$(ETCDIR):
	$(MKDIR) $@

$(ETCDIR)/%: % | $(ETCDIR)
	$(INSTALL_DATA) $< $@

install:
	cp -r $(ETCDIR) $(INST_DIR)
