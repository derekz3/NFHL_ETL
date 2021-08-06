#!/usr/bin/env python
import os
import sys
import json
import glob
import pandas as pd
from subprocess import Popen, PIPE
print(f"{sys.executable}\n")


# Run bash script from python with real-time output
# https://stackoverflow.com/questions/803265/getting-realtime-output-using-subprocess
def run(command, verbose=True):
    
    procExe = Popen(command, stdout=PIPE, stderr=PIPE)

    if verbose:
        while procExe.poll() is None:
            line = procExe.stdout.readline()
            # Decode utf-8 and workaround dumb formatting
            line = line.decode('utf-8')[:-1].replace('"','').strip('\n')
            print(line)
            
    stdout, stderr = procExe.communicate()
    if stderr: print(f"There was error: {stderr}")


def nfhl(dfirm, jump):

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
    print(f"{len(out)} flood zones acquired from DFIRM-ID {dfirm}.")


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
    # print(os.system("ls out"))

    
    # Reformat CSV file to format needed for React app
    df = pd.read_csv("out/polygon.csv")
    frame = pd.DataFrame({'col': []}) # Empty dataframe


    # Get each coordinate pair in '{lat: __, lng: __}' format
    for i in range(len(df)):
        empty_list = []
        dic = eval(df['geom'][i])
        for j in range(len(dic['coordinates'])):
            coord = dic['coordinates'][j]
            for k in range(len(coord)):
                empty_list.append({'lat': coord[k][1], 'lng': coord[k][0]})
        frame.loc[i] = str(empty_list)
    print("Geometry converted to '{lat: __, lng: __}' format")


    # Removes '' from the data
    frame2 = pd.DataFrame({'col': []})
    for i in range(len(frame)):
        frame2.loc[i] = frame.loc[i][0].replace("'", "")


    # Write out desired CSV file
    # run(['bash', '-c', 'rm out/polygon.csv && \
    #     echo "shapefile converted to CSV."'], False)
    frame2.to_csv("out/polygon_clean.csv")
    print("CSV cleaned!")


    # Copy files to host machine
    run(['bash', '-c', 'cp out/polygon_clean.csv /out/polygon_clean.csv'], False)
    run(['bash', '-c', 'cp out/polygon.csv /out/polygon.csv'], False)
    run(['bash', '-c', 'cp out/polygon.json /out/polygon.json'], False)
    run(['bash', '-c', 'cp -R shape /out/shape'], False)
    print("Files copied from container to host.")


# Make functions runnable from terminal
if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])
