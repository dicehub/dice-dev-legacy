#!/bin/sh

pyqt_base_dir="PyQt"
if [ ! -d $pyqt_base_dir ]; then
    mkdir -p $pyqt_base_dir
fi
cd $pyqt_base_dir

QMAKE="`pwd`/../Qt/bin/qmake" # must be the same as in build_qt.sh

pyqt_dir="PyQt-gpl-5.4.2"
pyqt_zip="PyQt-gpl-5.4.2.tar.gz"
pyqt_url="http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.4.2/PyQt-gpl-5.4.2.tar.gz"
parallel=4

PYTHON="`pwd`/../Python/bin/python3"

build() {
    echo "build PyQt5"
    cd "$pyqt_dir"
    "$PYTHON" configure.py --confirm-license --qmake="$QMAKE" --sip="../../Python/bin/sip"
    make -j$parallel
    make install
    cd ..
}

unpack() {
    echo "unpack"
    tar xf "$pyqt_zip"
}

get() {
    echo "get PyQt5"
    wget "$pyqt_url"
}

if [ -f "../Python/lib/python3.4/site-packages/PyQt5/QtCore.so" ]; then
    echo "PyQt5 installed"
elif [ -d "$pyqt_dir" ]; then
    build
elif [ -f "$pyqt_zip" ]; then
    unpack
    build
else
    get
    unpack
    build
fi