#!/bin/bash


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


cd sample
# Convert flood zone data from shapefile to GeoJSON-encoded geographies within a CSV
ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry) AS geom, * from S_FLD_HAZ_AR" polygon.csv S_FLD_HAZ_AR.shp


# conda deactivate
# conda env remove --name pipe