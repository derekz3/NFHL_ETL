#!/bin/bash


# Final output file
# FILE=out.json
# if [[ -f "$FILE" ]]; then
#     rm ${FILE}
#     touch ${FILE}
# else
#     touch ${FILE}
# fi


# Batch directory (intermediate output)
DIR=batches
if [[ -d "$DIR" ]]; then
    find ${DIR} -mindepth 1 -delete
else
    mkdir ${DIR}
fi


# Initialize global variables
PAGE=53 # Start near end of results to test process
LIMIT=100 # Number of results returned per request
FILTER="" # Additional filters (e.g. get 100 year flood plain) <----- Does not work lol
BASE_PRE="https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer/28/query?where=DFIRM_ID=%2706037C%27"
BASE_SUF="&f=geojson&resultRecordCount=100&resultOffset="


while true
do
    # Get number of characters in response with fast query (return IDs only)
    COUNT=$(( $PAGE * $LIMIT ))
    LEN_QUERY="${BASE_PRE}${FILTER}&outFields=FLD_AR_ID&returnGeometry=false${BASE_SUF}${COUNT}"
    LEN=$(curl -s -I $LEN_QUERY | head -2 | tail -1 | cut -d " " -f2)
    LEN=${LEN//[ $'\001'-$'\037']} # Remove all control chars
    if (( $LEN > 42 )); then # If response is greater than 42 chars, query is not empty
        # Return full set of features, including geography, and write to batch file
        FULL_QUERY="${BASE_PRE}${FILTER}&outFields=*&outSR=4326${BASE_SUF}${COUNT}"
        touch "${DIR}/batch${PAGE}.json"
        curl -s $FULL_QUERY >> "${DIR}/batch${PAGE}.json"
        # Report readable status
        echo "p.${PAGE} starts at item ${COUNT}."
        echo "p.${PAGE} complete ----------> ${COUNT} flood zones loaded!"
        echo "q.${PAGE} ${FULL_QUERY}"
        PAGE=$(( $PAGE+1 )) # next page
    else
        echo "End of results."
        break
    fi
done


echo "Begin post-processing batches."
# Combine batches into one json (dictionary) in conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate pipe
python3 fema.py


# Shapefile directory
DIR=shape
if [[ -d "$DIR" ]]; then
    find ${DIR} -mindepth 1 -delete
else
    mkdir ${DIR}
fi


# Convert GeoJSON to shapefile
ogr2ogr -f "ESRI Shapefile" ${DIR}/polygon.shp out.json


# Convert shapefile to GeoJSON-encoded geographies within a CSV
ogr2ogr -f csv -dialect sqlite -sql "select AsGeoJSON(geometry) AS geom, * from polygon" polygon.csv shape/polygon.shp
echo "Job done!"


# Next task: Convert geojson to csv


# Upload CSV file to Google Cloud Storage (GCS) bucket
    # Project ID: genuine-episode-317014
    # gsutil config -- how to automate?
    # gsutil mb -l us-east4 gs://nfhlbucket
    # gsutil -m cp sample/polygon.csv gs://nfhlbucket


# Upload CSV in GCS to BQ
    # Cloud URI: gs://nfhlbucket/polygon.csv
    # bq --location=us-east4 mk -d genuine-episode-317014:nfhlbq
    # bq load --autodetect --replace nfhlbq.polygon gs://nfhlbucket/polygon.csv


# bq rm -r -f -d genuine-episode-317014:nfhlbq
# gsutil rm -r gs://nfhlbucket