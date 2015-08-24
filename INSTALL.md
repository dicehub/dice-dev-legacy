HOW TO BUILD DICE
=================

System requirements
-------------------

- [Python 3.4.2](https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tar.xz)
- [Qt 5.4.1](http://www.qt.io/download/)
- [VTK 6.2.0](http://www.vtk.org/files/release/6.2/VTK-6.2.0.tar.gz)

Requirements:
-------------

- libxt-dev
- cmake
- liblapack3
- libgl1-mesa-dev
- build-essential

Linux:
------
Create build folder

    $ mkdir dice_build

Copy the following folders adn files from the root of the repository into **dice_build**:
   
    apps
    core
    core_apps
    db
    libview
    libvtk
    main
    test
    qt.conf
    thirdparty
    DICE.pro
    
Install Qt.

Copy content of **`<qt_install_path>/<version>/gcc_64/ into dice_build/thirdparty/Qt`**

Build python (including numpy, matplotlib and PyFoam), sip, pyqt and vtk by running inside **dice_build/thirdparty**:
    
    $ build_python.sh
    $ build_sip.sh
    $ build_pyqt5.sh
    $ build_vtk.sh
    $ strip_libs.sh
    $ clean_src.sh

or run:
    
    $ install.sh

Create make file by executing:

    $ <dice_build_path>/thirdparty/Qt/bin/qmake <dice_build_path>/DICE.pro -r -spec linux-g++

Run make in **dice_build**:

    $ make -r -w -j 4

Now install dice:

    $ make install
    
