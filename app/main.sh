#!/bin/bash
source utils.sh


# DOCKER COMMANDS
# Clean build: ... build --no-cache -t ...
: '
docker build -t ignite/conda:pipe .
docker run -it --rm --name piping -v $(pwd)/out:/out ignite/conda:pipe /bin/bash
docker rmi -f ignite/conda:pipe
'


# Pagination strategy for FEMA API calls
function call {

    # Reset output files and directories
    empty out
    empty pages
    empty shape
    remove polygon.csv
    remove polygon.json

    # Initialize global variables
    PAGE=$(( $1 )) # Start collecting at this page
    LIMIT=100 # Number of results returned per request

    # Specify FEMA API calls
    DIR="https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer/28/"
    PAGING="&resultRecordCount=100&resultOffset="
    WHERE=$2
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
            PAGE=$(( $PAGE + 1 )) # Next page
        else
            echo "End of results."
            break
        fi
    done
}


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
