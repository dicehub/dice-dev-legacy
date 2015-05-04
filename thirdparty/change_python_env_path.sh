OLD="#!/home/build/DICEv0.0.1/thirdparty/Python/Python-3.4.2/../bin/python3.4"
NEW="#!../Python/bin/python3.4"

cd Python
find bin/. -type f -exec sed -i 's|'$OLD'|'$NEW'|g' {} +
cd ..