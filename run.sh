#!/bin/bash


# Simplify process for calling pipeline
# getops tutorial: https://archive.is/TRzn4
# Reference: https://stackoverflow.com/questions/12022592/how-can-i-use-long-options-with-the-bash-getopts-builtin
function pipeline {

    # Open Docker if it isn't running
    if (! docker stats --no-stream &> /dev/null ); then

        # On MacOS, this is the terminal command to launch Docker
        open /Applications/Docker.app

        # Wait until Docker daemon is running and has completed initialisation
        while (! docker stats --no-stream &> /dev/null ); do
            echo "Waiting for Docker to launch..."
            sleep 1
        done
    fi

    # Initialize Docker build command
    BUILD_STR="docker build -t ignite/conda:pipe"

    # Check if options were passed
    if [ ! $# -eq 0 ]; then
        echo "options were passed"

        # Transform long options to short ones
        for arg in "$@"; do
            shift
            case "$arg" in
                "--DFIRM") set -- "$@" "-d" ;;
                "--JUMP")  set -- "$@" "-j" ;;
                *)         set -- "$@" "$arg"
            esac
        done

        # Default behavior
        rest=false; ws=false

        # Parse short options
        OPTIND=1
        while getopts "d:j:" opt; do # : indicates arguments are expected
            case $opt in
                d) 
                    BUILD_STR="${BUILD_STR} --build-arg DFIRM=$OPTARG" 
                    # echo "-d was triggered, Parameter: $OPTARG" >&2
                    ;;
                j) 
                    BUILD_STR="${BUILD_STR} --build-arg JUMP=${OPTARG}" 
                    # echo "-j was triggered, Parameter: $OPTARG" >&2
                    ;;
                \?)
                    echo "Invalid option: -$OPTARG" >&2
                    exit 1
                    ;;
            esac
        done
        shift $(expr $OPTIND - 1) # remove options from positional parameters
        # shift $((OPTIND - 1))
    fi

    # Build container from specified docker image
    BUILD() { echo "$BUILD_STR ."; }
    echo "$BUILD_STR ."
    eval $(BUILD)

    # Run docker container in interactive terminal
    docker run -it --name piping -v $(pwd)/out:/out ignite/conda:pipe /bin/bash
}

if [[ $1 == "pipeline" ]]; then
    eval "${@}"
fi


# Test command line parsing
: '
source run.sh && pipeline
source run.sh && pipeline --DFIRM 6011C
./run.sh pipeline --DFIRM 6011C
./run.sh pipeline --JUMP 50
./run.sh pipeline --DFIRM 6011C --JUMP 50
./run.sh pipeline --JUMP 50 --DFIRM 6011C
'
