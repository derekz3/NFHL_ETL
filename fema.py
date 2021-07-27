#!/usr/bin/python


import json
import glob


# Initialize global variables/data
batches = glob.glob('batches/*')
out = []
start = 53 # for testing purposes


for index, batch in enumerate(batches):
    page = index + start
    f = open('batches/batch' + str(page) + '.json',)
    fdict = json.load(f)
    print(f"batch{page}: {len(fdict['features'])}")
    out = out + fdict['features']
    f.close()
print(f"Total: {len(out)}")

with open("out.json", "w+") as f:
    json.dump({"type": "FeatureCollection", \
               "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::4269" } }, \
               "features": out}, f, indent=4)
    f.close()