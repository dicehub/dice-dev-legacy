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

if [ -f "js_lib/5.3.0.tar.gz" ]; then
    echo "codemirror installed"
else
	get_codemirror
fi