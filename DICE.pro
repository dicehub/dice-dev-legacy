# --------------------------------------
# File for qmake to generate a Makefile.
# --------------------------------------

TARGET = DICE
DESTDIR = $$(PWD)
#message(The project will be installed in $$DESTDIR)

VERSION = _0.0.3

TEMPLATE = subdirs
SUBDIRS = libvtk main

main.depends = libvtk


QML_IMPORT_PATH = libview

OTHER_FILES += \
                README.md \
                LICENSE.md \
                INSTALL.md \
                DICE.pro \
                qt.conf


for(FILE, OTHER_FILES){
    copydata.commands += $(COPY_DIR) $$PWD/$${FILE} $$OUT_PWD$$escape_expand(\\n\\t)
}
    first.depends = $(first) copydata
    export(first.depends)
    export(copydata.commands)
    QMAKE_EXTRA_TARGETS += first copydata
