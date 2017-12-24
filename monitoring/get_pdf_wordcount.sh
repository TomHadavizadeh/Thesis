#!/bin/bash

file=../thesis_v0.pdf 
if (( "${#1}" > "5" )); then
    file=$1
fi
pdftotext $file - | egrep -o '[a-zA-Z]+' | egrep -e '\w\w+' | wc -w
