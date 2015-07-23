#!/bin/sh

js_lib_dir="js_lib"
if [ ! -d $js_lib_dir ]; then
    mkdir -p $js_lib_dir
fi
cd $js_lib_dir

get_bootstrap() {
	bootrsap_url="https://github.com/twbs/bootstrap/archive/v3.3.2.tar.gz"
	bootstrap_zip="v3.3.2.tar.gz"
	echo "Get bootstrap"
	wget "$bootrsap_url"
	echo "unpack"
    tar xf "$bootstrap_zip"
}

if [ -f "js_lib/bootstrap-3.3.2-dist" ]; then
    echo "bootstrap installed"
else
	get_bootstrap
fi


get_codemirror() {
	codemirror_url="https://github.com/codemirror/CodeMirror/archive/5.3.0.tar.gz"
	codemirror_zip="5.3.0.tar.gz"
	echo "Get codemirror"
	wget "$codemirror_url"
	echo "unpack"
    tar xf "$codemirror_zip"
}

if [ -f "js_lib/CodeMirror-5.3.0" ]; then
    echo "codemirror installed"
else
	get_codemirror
fi


get_open_sans_font() {
	open_sans_font_url="https://github.com/FontFaceKit/open-sans/archive/1.4.2.tar.gz"
	open_sans_font_zip="1.4.2.tar.gz"
	echo "Get Open Sans Font"
	wget "$open_sans_font_url"
	echo "unpack"
    tar xf "$open_sans_font_zip"
}

if [ -f "js_lib/open-sans-1.4.2" ]; then
    echo "Open Sans Font installed"
else
	get_open_sans_font
fi