#!/bin/bash                                                                     
export PYTHONPATH=/home/nugrid

#IPN_URL="https://github.com/swjones/nugridnotebooks.git"
IPN_URL="https://github.com/fherwig/nugridnotebooks.git"
IPN_LOCAL="/home/nugrid/nugridnotebooks"
IPN_DIR="${IPN_LOCAL}/notebooks"

[[ -d ${IPN_DIR} ]] || git clone ${IPN_URL} ${IPN_LOCAL}

# add Luke's widget module to python path:
export PYTHONPATH=${IPN_LOCAL}/modules:$PYTHONPATH

ipython notebook \
    --profile=nbserver \
    --no-browser \
    --ip=0.0.0.0 \
    --port=8888 \
    --notebook-dir=${IPN_DIR}

