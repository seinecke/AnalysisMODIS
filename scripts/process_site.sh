#!/bin/bash

source activate modis

mkdir $1

python scripts/ProcessImages.py "M*D06_L2/2015/*/*.hdf" -l $1 -f $1/ -o 2015.csv --maps
python scripts/ProcessImages.py "M*D06_L2/2016/*/*.hdf" -l $1 -f $1/ -o 2016.csv --maps
python scripts/ProcessImages.py "M*D06_L2/2017/*/*.hdf" -l $1 -f $1/ -o 2017.csv --maps
python scripts/ProcessImages.py "M*D06_L2/2018/*/*.hdf" -l $1 -f $1/ -o 2018.csv --maps
python scripts/ProcessImages.py "M*D06_L2/2019/*/*.hdf" -l $1 -f $1/ -o 2019.csv --maps
