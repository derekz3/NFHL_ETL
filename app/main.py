#!/usr/bin/env python
import sys
import json
import glob
from subprocess import Popen, PIPE
print(sys.executable)


# Run bash script from python with real-time output
# https://stackoverflow.com/questions/803265/getting-realtime-output-using-subprocess
def run(command, verbose=True):
    
    procExe = Popen(command, stdout=PIPE, stderr=PIPE)

    if verbose:
        while procExe.poll() is None:
            line = procExe.stdout.readline()
            # Decode utf-8 and workaround dumb formatting
            line = line.decode('utf-8')[:-1].replace('"','')
            print(line)
            
    stdout, stderr = procExe.communicate()
    if stderr: print(f"There was error: {stderr}")


def nfhl(dfirm, jump):

    # Load data from API calls
    nfhl_loc = 'source main.sh && call ' + str(jump) + ' ' + str(dfirm)
    run(['bash', '-c', nfhl_loc])
    print("Begin post-processing pages.")


    # Initialize global variables/data
    pages = glob.glob('pages/*')
    start = int(jump) # for testing purposes
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
    run(['bash', '-c', 'export CPL_LOG=/dev/null && ogr2ogr -f "ESRI Shapefile" shape/polygon.shp out/polygon.json'])


    # Convert shapefile to GeoJSON-encoded geographies within a CSV
    run(['bash', '-c', 'ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry) AS geom, * from polygon" out/polygon.csv shape/polygon.shp'])


    # Copy files to host machine
    run(['bash', '-c', 'cp out/polygon.csv /out/polygon.csv'], False)
    run(['bash', '-c', 'cp out/polygon.json /out/polygon.json'], False)
    run(['bash', '-c', 'cp -R shape /out/shape'], False)


# Make functions runnable from terminal
if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])
