# Analysis MODIS

## Installation

It is recommended to create a dedicated conda environment for this.
In the following it is assumed that you have a conda environment called `modis`.

## Processing

Go to `https://ladsweb.modaps.eosdis.nasa.gov/search/` and select your data to be analysed. 
Download the query as csv.

To process, you can use `run.sh` like this:

```
bash scripts/run.sh queries/LAADS_query.2019-04-17T00_22.csv
```

This will create 3 folders (Adelaide, Arkaroola, Barmera).
For each location cloud maps and a csv with dates and mean cloudiness are derived.

## Scripts

### create_download.py

python create_download.py query.csv

This will download all you selected data. Selected data from your query is stored in query.csv.

### download.sh


### ProcessImages.py

