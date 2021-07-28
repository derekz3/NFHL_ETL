#!/usr/bin/python


import json
import glob


# Initialize global variables/data
batches = glob.glob('batches/*')
out = []
start = 53 # for testing purposes


# Loop through batch files and append records into list
for index, batch in enumerate(batches):
    f = open('batches/batch' + str(index + start) + '.json',)
    page = json.load(f)
    print(f"batch{index + start}: {len(page['features'])}")
    out = out + page['features']
    f.close()
print(f"Total: {len(out)}")


# Convert list elements to json strings and write to file
with open("polygon.json", 'w+') as f:
    f.write('\n'.join(map(json.dumps, out)))
    f.close()


# Initial approach
# with open("polygon.json", "w+") as f:
#     json.dump({"type": "FeatureCollection", \
#                "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::4269" } }, \
#                "features": out}, f, indent=2)
#     f.close()