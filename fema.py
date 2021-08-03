#!/usr/bin/env python
import os
import sys
import json
import glob
from pathlib import Path
print(sys.executable)


# Get directories
app = os.getcwd()
home = str(Path.home())


# Initialize global variables/data
pages = glob.glob('pages/*')
start = 53 # for testing purposes
out = []


# Loop through page files and append records into list
for index in range(len(pages)):
    f = open('pages/page' + str(index + start) + '.json',)
    page = json.load(f)
    print(f"p.{index + start}: {len(page['features'])}")
    out = out + page['features']
    f.close()
print(f"Total: {len(out)}")


# Convert list elements to json strings and write to file
with open("polygon.json", 'w+') as f:
    f.write('\n'.join(map(json.dumps, out)))
    f.close()

os.system('ogr2ogr -f "ESRI Shapefile" shape/polygon.shp polygon.json')
os.system('ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry) AS geom, * from polygon" polygon.csv shape/polygon.shp')