#!/bin/bash

source activate modis

python scripts/create_download.py $1
bash download.sh

mkdir Adelaide
mkdir Arkaroola
mkdir Barmera

# Assuming entire year. We shoudl consider dividing in single months or so.
# this should be done via the LADS csv I guess
python scripts/ProcessImages.py "MYD06_L2/2018/*/*.hdf" -l Adelaide -f Adelaide/ -o 2018.csv
python scripts/ProcessImages.py "MYD06_L2/2018/*/*.hdf" -l Arkaroola -f Arkaroola/ -o 2018.csv
python scripts/ProcessImages.py "MYD06_L2/2018/*/*.hdf" -l Barmera -f Barmera/ -o 2018.csv

# in case you want to automatically remove the files afterwards
#rm -r MYD06_L2
