#!/bin/bash
# File for common bash utility functions


# Empty directory (or create if non-existant)
function empty {
    DIR=$1
    if [[ -d "$DIR" ]]; then
        find ${DIR} -mindepth 1 -delete
    else
        mkdir ${DIR}
    fi
}


# Remove file
function remove {
    FILE=$1
    if [[ -f "$FILE" ]]; then 
        rm ${FILE}
    fi
}

# Remove directory
function remove_dir {
    DIR=$1
    if [[ -d "$DIR" ]]; then 
        rm -r ${DIR}
    fi
}


# Print readable report
function report {
    PAGE=$1
    COUNT=$2
    LIMIT=$3
    FULL_QUERY=$4
    echo "pg.${PAGE} complete!"
    # echo "p.${PAGE}: Starts at item ${COUNT}."
    # echo "p.${PAGE}: $(( $COUNT + $LIMIT )) flood zones loaded!"
    # echo "p.${PAGE}: ${FULL_QUERY}"
    # echo ""
}
