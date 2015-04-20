#!/bin/sh

py_base_dir="Python"
if [ ! -d $py_base_dir ]; then
    mkdir -p $py_base_dir
fi
cd $py_base_dir

py_dir="Python-3.4.2"
py_zip="Python-3.4.2.tar.xz"
py_url="https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tar.xz"
parallel=4

# open_ssl_url="https://openssl.org/source/openssl-1.0.2.tar.gz"
# open_ssl_zip="openssl-1.0.2.tar.gz"
# open_ssl_dir="openssl-1.0.2"

# build_openssl() {
#   wget "$open_ssl_url"
#   tar -xvzf "$open_ssl_zip"
#   cd "$open_ssl_dir"
#   ./config shared --prefix="`pwd`/.." --openssldir="`pwd`/../openssl"
#   make -j$parallel
#   make install
#   cd ..
# }

buildpackages() {
    ./bin/pip3 install docutils
    ./bin/pip3 install numpy
    ./bin/pip3 install matplotlib
    ./bin/pip3 install PyFoam
}

build() {
    echo "build python"
    cd "$py_dir"
#     export LDFLAGS="-L`pwd`/../lib/"
#     export LD_LIBRARY_PATH="`pwd`/../lib/:`pwd`/../lib/"
#     export CPPFLAGS="-I`pwd`/../include -I`pwd`/../include/openssl"
    ./configure --with-threads --enable-shared --prefix="`pwd`/.." --with-ensurepip=install
    make -j$parallel
    make install
    cd ..
}

unpack() {
    echo "unpack"
    tar xf "$py_zip"
}

get() {
    echo "get python"
    wget "$py_url"
}

if [ -f "bin/python3" ]; then
    echo "python installed"
elif [ -d "$py_dir" ]; then
    build
    buildpackages
elif [ -f "$py_zip" ]; then
    unpack
    build
    buildpackages
else
    get
    unpack
    build
    buildpackages
fi