#!/bin/sh

sip_base_dir="Sip"
if [ ! -d $sip_base_dir ]; then
    mkdir -p $sip_base_dir
fi
cd $sip_base_dir

sip_dir="sip-4.16.8"
sip_zip="sip-4.16.8.tar.gz"
sip_url="http://sourceforge.net/projects/pyqt/files/sip/sip-4.16.8/sip-4.16.8.tar.gz"
parallel=4

PYTHON="`pwd`/../Python/bin/python3"

build() {
    echo "build Sip"
    cd "$sip_dir"
    "$PYTHON" configure.py
    make -j$parallel
    make install
    cd ..
}

unpack() {
    echo "unpack"
    tar xf "$sip_zip"
}

get() {
    echo "get Sip"
    wget "$sip_url"
}

if [ -f "../Python/bin/sip" ]; then
    echo "sip installed"
elif [ -d "$sip_dir" ]; then
    build
elif [ -f "$sip_zip" ]; then
    unpack
    build
else
    get
    unpack
    build
fi