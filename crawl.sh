#!/bin/bash


# Shapefile directory
if [[ -d shape ]]; then
    find shape -mindepth 1 -delete
else
    mkdir shape
fi


# Reset output files and directories
if [[ -d batches ]]; then rm -r batches; fi
if [[ -f polygon.csv ]]; then rm polygon.csv; fi
if [[ -f polygon.json ]]; then rm polygon.json; fi


# Install Google Chrome
CHROME=$(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version)
GREQ='Google Chrome 92.' # require Google Chrome >= 92.0.4515
if [[ "$CHROME" != *"$GREQ"* ]]; then
  wget https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg
  open ~/Downloads/googlechrome.dmg
  sudo cp -r /Volumes/Google\ Chrome/Google\ Chrome.app /Applications/
  rm googlechrome.dmg
fi


# Run python scripts in conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate pipe
python3 crawl.py


# Convert shapefile to GeoJSON-encoded geographies within a CSV
ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry) AS geom, * from S_FLD_HAZ_AR" polygon.csv shape/S_FLD_HAZ_AR.shp


# Upload CSV file to Google Cloud Storage (GCS) bucket
    # Project ID: genuine-episode-317014
    # gsutil config -- how to automate?
    # gsutil mb -l us-east4 gs://nfhlbucket
    # gsutil -m cp polygon.csv gs://nfhlbucket


# Upload CSV in GCS to BQ
    # Cloud URI: gs://nfhlbucket/polygon.csv
    # bq --location=us-east4 mk -d genuine-episode-317014:nfhlbq
    # bq load --autodetect --replace nfhlbq.polygon gs://nfhlbucket/polygon.csv


# bq rm -r -f -d genuine-episode-317014:nfhlbq
# gsutil rm -r gs://nfhlbucket


# conda deactivate
# conda env remove --name pipe