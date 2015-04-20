#!/bin/bash

for l in Python/lib/*; do
    strip "$l"
done

for l in Qt/lib/*; do
    strip "$l"
done

for l in vtk/lib/*; do
    strip "$l"
done