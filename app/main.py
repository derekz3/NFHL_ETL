#!/usr/bin/env python
import sys
import json
import glob
from utils import *
print(f"{sys.executable}\n")


# Make pipeline extensible
def nfhl(dfirm, jump):

    csv_max()

    # Load data from API calls
    nfhl_loc = 'source main.sh && call ' + str(jump) + ' ' + str(dfirm)
    run(['bash', '-c', nfhl_loc])
    print("Post-processing data:")

    # Initialize global variables/data
    pages = glob.glob('pages/*')
    start = int(jump) # for testing purposes
    out = []

    # Loop through page files and append records into list
    for index in range(len(pages)):
        f = open('pages/page' + str(index + start) + '.json',)
        page = json.load(f)
        out = out + page['features']
        f.close()
    num_zones = len(out)
    print(f"{num_zones} flood zones acquired from DFIRM-ID {dfirm}.")

    # Convert list elements to json strings and write to file
    with open("out/polygon.json", 'w+') as f:
        f.write('\n'.join(map(json.dumps, out)))
        f.close()

    # Convert GeoJSON to shapefile
    run(['bash', '-c', 'export CPL_LOG=/dev/null && \
        ogr2ogr -f "ESRI Shapefile" shape/polygon.shp out/polygon.json'], False)
    print("JSON converted to shapefile.")
    
    # Convert shapefile to GeoJSON-encoded geographies within a CSV
    run(['bash', '-c', 'ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry) AS geom, \
        * from polygon" out/polygon.csv shape/polygon.shp'], False)
    print("shapefile converted to CSV.")

    # Clean CSV file
    clean(num_zones)
    print(f"{num_zones}/{num_zones} rows processed.")
    print("CSV cleaned!")

    # Copy files to host machine
    # run(['bash', '-c', 'cp out/polygon.csv /out/polygon.csv'], False)
    # run(['bash', '-c', 'cp out/polygon.json /out/polygon.json'], False)
    run(['bash', '-c', 'cp -R shape /out/shape'], False)
    # run(['bash', '-c', 'cp out/polygon_clean.csv /out/polygon_clean.csv'], False)
    # run(['bash', '-c', 'cp out/polygon_write.csv /out/polygon_write.csv'], False)
    run(['bash', '-c', 'cp out/100yr.csv /out/100yr.csv'], False)
    run(['bash', '-c', 'cp out/500yr.csv /out/500yr.csv'], False)
    print("Files copied from container to host.")
    return


# Make functions runnable from terminal
if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])
