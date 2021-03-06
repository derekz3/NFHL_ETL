#!/bin/bash
source app/utils.sh


# Simplify process for calling pipeline
# getops tutorial: https://archive.is/TRzn4
# Reference: https://stackoverflow.com/questions/12022592/how-can-i-use-long-options-with-the-bash-getopts-builtin
function pipeline {

    # Check if Docker is installed
    # Reference: https://www.digitalocean.com/community/questions/how-to-check-for-docker-installation
    # Reference: https://stackoverflow.com/questions/32744780/install-docker-toolbox-on-a-mac-via-command-line
    docker -v
    if (( $? == 0 )); then
        echo "Docker installed."
    else 
        # Install Homebrew
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

        # Install Docker for M1-MAC
        brew install --cask docker
        echo "Docker installed."
    fi

    # Get system memory limit for Docker
    MEM=$(grep -hnr "memoryMiB" /Users/$(id -un)/Library/Group\ Containers/group.com.docker/settings.json | sed 's/.* \(.*\),/\1/')

    # If limit is not 10gb, change to 10gb
    if (( $MEM < 10240 )); then

        echo "Docker system memory limit too low. ("${MEM}gb")"

        # Kill Docker processes
        # Reference: https://stackoverflow.com/questions/41449827/how-to-restart-docker-for-mac-with-command
        killall -HUP com.docker.hyperkit
        echo "Killed Docker."

        # Set total runtime memory limit for Docker (not container) running on host machine's system
        # Reference: https://stackoverflow.com/questions/42402825/how-to-set-dockers-system-memory/50398665
        # Reference: https://stackoverflow.com/questions/44533319/how-to-assign-more-memory-to-docker-container
        sed -i "" "s/$MEM/10240/g" /Users/$(id -un)/Library/Group\ Containers/group.com.docker/settings.json &> /dev/null
    fi

    # Open Docker if it is not running
    if (! docker stats --no-stream &> /dev/null ); then

        # On MacOS, this is the terminal command to launch Docker
        open /Applications/Docker.app # or open -a Docker?

        # Wait until Docker daemon is running and has completed initialisation
        while (! docker stats --no-stream &> /dev/null); do
            echo "Waiting for Docker to launch..."
            sleep 1
        done
    fi

    # Reset docker image and container + output directory as needed
    # Reference: https://stackoverflow.com/questions/38576337/how-to-execute-a-bash-command-only-if-a-docker-container-with-a-given-name-does
    ! docker container inspect piping &> /dev/null || docker rm -f -v piping &> /dev/null
    ! docker image inspect ignite/conda:pipe &> /dev/null || docker rmi -f ignite/conda:pipe &> /dev/null
    clear

    # Initialize Docker build command
    BUILD_STR="DOCKER_BUILDKIT=1 docker build -t ignite/conda:pipe"

    # Check if options were passed
    if [ ! $# -eq 0 ]; then
        echo "" ; echo "Options were passed."

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
                    echo "-d was triggered, Parameter: $OPTARG" >&2
                    ;;
                j) 
                    BUILD_STR="${BUILD_STR} --build-arg JUMP=${OPTARG}" 
                    echo "-j was triggered, Parameter: $OPTARG" >&2
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
    echo "$BUILD_STR ." && echo ""
    eval $(BUILD)

    # Run docker container in interactive terminal
    # docker run --rm -it --name piping -v $(pwd)/out:/out ignite/conda:pipe /bin/bash
    docker run --rm -it --memory="5g" --memory-swap="6g" --oom-kill-disable --cpus="4" --name piping -v $(pwd)/out:/out ignite/conda:pipe /bin/bash

    # Exit code: success
    exit 0 &> /dev/null
}


# Clear files generated by running the pipeline
function clear {
    remove_dir out/shape
    remove out/polygon.json
    remove out/polygon.csv
    remove out/polygon_clean.csv
    remove out/polygon_write.csv
    remove out/100yr.csv
    remove out/500yr.csv
}


# Make pipeline callable from terminal w/o sourcing
# Reset output directory from terminal w/o sourcing
if [[ $1 == "pipeline" ]]; then
    eval "${@}"
elif [[ $1 == "clear" ]]; then
    clear
fi


# Test command line parsing
: '
source run.sh && pipeline
source run.sh && pipeline --DFIRM 06111C
./run.sh pipeline

./run.sh pipeline --DFIRM 06111C
./run.sh pipeline --JUMP 30
./run.sh pipeline --DFIRM 06111C --JUMP 30
./run.sh pipeline --JUMP 30 --DFIRM 06111C

./run.sh pipeline -d 06111C
./run.sh pipeline -j 30
./run.sh pipeline -d 06111C -j 30
./run.sh pipeline -j 30 -d 06111C
'
