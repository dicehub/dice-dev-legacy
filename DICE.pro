# --------------------------------------
# File for qmake to generate a Makefile.
# --------------------------------------

TEMPLATE = subdirs
SUBDIRS = libvtk main

main.depends = libvtk


QML_IMPORT_PATH = libview

OTHER_FILES += qt.conf \
                README.md \
                LICENSE.md \
                INSTALL.md


for(FILE, OTHER_FILES){
    copydata.commands += $(COPY_DIR) $$PWD/$${FILE} $$OUT_PWD$$escape_expand(\\n\\t)
}
    first.depends = $(first) copydata
    export(first.depends)
    export(copydata.commands)
    QMAKE_EXTRA_TARGETS += first copydata
