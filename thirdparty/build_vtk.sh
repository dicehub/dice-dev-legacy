#!/bin/sh

vtk_base_dir="vtk"
if [ ! -d $vtk_base_dir ]; then
    mkdir -p $vtk_base_dir
fi
cd $vtk_base_dir

vtk_dir="VTK-6.2.0"
vtk_zip="VTK-6.2.0.tar.gz"
vtk_url="http://www.vtk.org/files/release/6.2/VTK-6.2.0.tar.gz"
parallel=4

# missing libraries: vtkViewsGeovis, vtkRenderingVolumeAMR

build() {
    echo "build vtk"
    cd "$vtk_dir"
    mkdir -p build
    cd build
    cmake .. -DVTK_Group_Imaging=ON -DVTK_Group_MPI=ON -DVTK_Group_Rendering=ON -DVTK_Group_StandAlone=ON -DCMAKE_INSTALL_PREFIX=../..
    make -j$parallel
    make install
    cd ../..
}

unpack() {
    echo "unpack"
    tar xf "$vtk_zip"
}

get() {
    echo "get vtk"
    wget "$vtk_url"
}

if [ -f "$vtk_dir/lib/libvtkCommonCore-6.2.so" ]; then
    echo "vtk installed"
elif [ -d "$vtk_dir" ]; then
    build
elif [ -f "$vtk_zip" ]; then
    unpack
    build
else
    get
    unpack
    build
fi