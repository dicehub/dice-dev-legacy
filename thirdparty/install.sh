#!/bin/sh

if [ -f "Python/bin/python3" ]; then
    echo "Python installed"
else
    ./build_python.sh
fi

if [ -f "Python/bin/sip" ]; then
    echo "Sip installed"
else
    ./build_sip.sh
fi

if [ -f "Python/lib/python3.4/site-packages/PyQt5/QtCore.so" ]; then
    echo "PyQt installed"
else
    ./build_pyqt5.sh
fi

if [ -f "vtk/lib/libvtkCommonCore-6.2.so" ]; then
    echo "VTK installed"
else
    ./build_vtk.sh
fi

./clean_src.sh
./strip_libs.sh