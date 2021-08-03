#!/bin/bash
source utils.sh

# docker pull osgeo/gdal:alpine-normal-latest-arm64
# docker run -it osgeo/gdal:alpine-normal-latest-arm64 /bin/sh
# docker cp pipeline/. 2483cb7f9a0a:/bin

# docker build .
# docker run -it b1763df39e33 /bin/sh
# apk
# apk add curl

# Reset output files and directories
empty pages
empty shape
remove polygon.csv
remove polygon.json


# Initialize global variables
PAGE=53 # Start near end of results to test process
LIMIT=100 # Number of results returned per request


# Specify FEMA API calls
DIR="https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer/28/"
PAGING="&resultRecordCount=100&resultOffset="
WHERE="06037C"
FORMAT="geojson"
BASE="${DIR}query?where=DFIRM_ID=%27${WHERE}%27&f=${FORMAT}${PAGING}"
LEN_DIFF="&outFields=FLD_AR_ID&returnGeometry=false"
FULL_DIFF="&outFields=*&outSR=4326"


while true
do
    # Get number of characters in response with fast query (return IDs only)
    COUNT=$(( $PAGE * $LIMIT ))
    LEN_QUERY="${BASE}${COUNT}${LEN_DIFF}"
    LEN=$(curl -s -I $LEN_QUERY | head -2 | tail -1 | cut -d " " -f2)
    LEN=${LEN//[ $'\001'-$'\037']} # Remove all control chars from parsed HTTP header
    if (( $LEN > 42 )); then # If response is greater than 42 chars, query is not empty
        # Return full set of features, including geography, and write to page file
        FULL_QUERY="${BASE}${COUNT}${FULL_DIFF}"
        touch "pages/page${PAGE}.json"
        curl -s $FULL_QUERY >> "pages/page${PAGE}.json"
        report $PAGE $COUNT $LIMIT $FULL_QUERY
        PAGE=$(( $PAGE + 1 )) # next page
    else
        echo "End of results."
        break
    fi
done


# Combine pages into one json (dictionary)
echo "Begin post-processing pages."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate pipe
python3 fema.py


# Convert GeoJSON to shapefile
# ogr2ogr -f "ESRI Shapefile" shape/polygon.shp polygon.json


# Convert shapefile to GeoJSON-encoded geographies within a CSV
# ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry) AS geom, * from polygon" polygon.csv shape/polygon.shp
echo "Job done!"


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