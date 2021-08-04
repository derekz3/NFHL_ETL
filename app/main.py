#!/usr/bin/env python
import sys
import json
import glob
from subprocess import Popen, PIPE
print(sys.executable)


# Run bash script from python with real-time output
# https://stackoverflow.com/questions/803265/getting-realtime-output-using-subprocess
def prun(command):
    procExe = Popen(command, stdout=PIPE, stderr=PIPE)
    while procExe.poll() is None:
        line = procExe.stdout.readline()
        # Decode utf-8 and workaround dumb formatting
        line = line.decode('utf-8')[:-1].replace('"','')
        print(line)
    stdout, stderr = procExe.communicate()
    if stderr: print(f"There was error: {stderr}")


# Load data from API calls
prun(['bash', '-c', 'source main.sh && call 53 06037C'])
print("Begin post-processing pages.")


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
with open("out/polygon.json", 'w+') as f:
    f.write('\n'.join(map(json.dumps, out)))
    f.close()


# Convert GeoJSON to shapefile
prun(['bash', '-c', 'export CPL_LOG=/dev/null && ogr2ogr -f "ESRI Shapefile" shape/polygon.shp out/polygon.json'])


# Convert shapefile to GeoJSON-encoded geographies within a CSV
prun(['bash', '-c', 'ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry) AS geom, * from polygon" out/polygon.csv shape/polygon.shp'])


# Copy files to host machine
prun(['bash', '-c', 'cp out/polygon.csv /out/polygon.csv'])
prun(['bash', '-c', 'cp out/polygon.json /out/polygon.json'])
prun(['bash', '-c', 'cp -R shape /out/shape'])
