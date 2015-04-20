#!/bin/sh

py_dir="PyFoam-0.6.4"
py_zip="PyFoam-0.6.4.tar.gz"
py_url="http://openfoamwiki.net/images/3/3b/PyFoam-0.6.4.tar.gz"
parallel=4

PYTHON="`pwd`/bin/python3"

build() {
    echo "build PyFoam"
    cd "$py_dir"
    "$PYTHON" setup.py install
    cd ..
}

unpack() {
    echo "unpack"
    tar xf "$py_zip"
}

get() {
    echo "get PyFoam"
    wget "$py_url"
}

if [ -f "lib/python3.4/site-packages/PyFoam/__init__.py" ]; then
    echo "PyFoam installed"
elif [ -d "$py_dir" ]; then
    build
elif [ -f "$py_zip" ]; then
    unpack
    build
else
    get
    unpack
    build
fi