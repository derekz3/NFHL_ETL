import sys
import csv
from subprocess import Popen, PIPE
# Helper methods for cleaning polygon data


# Reformat CSV file to format needed for React app
def clean(num_zones):

    # Write formatted lines to new CSV one by one 
    # with open('out/polygon.csv', 'r') as f, open('out/polygon_write.csv', 'w+') as o:
    with open('out/polygon.csv', 'r') as f, open('out/100yr.csv', 'w+') as o, open('out/500yr.csv', 'w+') as v:
        # o.write('FLD_ZONE,ZONE_SUBTY,geom\n')
        # v.write('FLD_ZONE,ZONE_SUBTY,geom\n')
        reader = csv.reader(f)
        next(reader) # skip header row

        for i, row in enumerate(reader):
            if (i % 100) == 0: print(f"{i}/{num_zones} rows processed.")

            vertices = []
            FLD_ZONE = row[6]
            ZONE_SUBTY = row[7]
            if ZONE_SUBTY == "": ZONE_SUBTY = "NaN"
            polygons = eval(row[0])['coordinates']

            # Get each coordinate pair in '{lat: __, lng: __}' format
            refactor_coordinates(polygons, vertices)

            # enter = format_row(FLD_ZONE, ZONE_SUBTY, str(vertices).replace("'", ""))
            enter = str(vertices).replace("'", "").replace(" ", "") + '\n'
            
            # o.write(enter)
            if (check_100yr(FLD_ZONE)): o.write(enter)
            if (check_500yr(ZONE_SUBTY)): v.write(enter)

        f.close()
        o.close()
    
    return


# Get each coordinate pair in '{lat: __, lng: __}' format
def refactor_coordinates(polygons, vertices):
    for j in range(len(polygons)):
        polygon = polygons[j]
        for k in range(len(polygon)):
            vertex = polygon[k]
            vertices.append({'lat':vertex[1],'lng':vertex[0]})


# Check if flood zone belongs to 100 year flood plain (1%)
def check_100yr(FLD_ZONE):
    if (FLD_ZONE == "A" or 
        FLD_ZONE == "AE" or 
        FLD_ZONE == "AO" or 
        FLD_ZONE == "AH"
       ): return True
    else: return False


# Check if flood zone belongs to 500 year flood plain (0.2%)
def check_500yr(ZONE_SUBTY):
    if (ZONE_SUBTY == "0.2 PCT ANNUAL CHANCE FLOOD HAZARD"): 
        return True
    else: 
        return False


# Final format for each CSV line
# def format_row(FLD_ZONE, ZONE_SUBTY, vertices):
#     return f'{FLD_ZONE},{ZONE_SUBTY},{vertices}\n'


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
    return


# Set csv.field_size_limit to max value (large fields are expected)
# Reference: https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
# Reference: https://stackoverflow.com/questions/19189522/what-does-killed-mean-when-a-processing-of-a-huge-csv-with-python-which-sudde
def csv_max():

    maxInt = sys.maxsize
    while True:
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)
