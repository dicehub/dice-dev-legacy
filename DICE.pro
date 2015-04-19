# --------------------------------------
# File for qmake to generate a Makefile.
# --------------------------------------

TEMPLATE = subdirs
SUBDIRS = libvtk main

main.depends = libvtk


QML_IMPORT_PATH = libview
