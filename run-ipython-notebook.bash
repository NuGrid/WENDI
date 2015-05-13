#!/bin/bash                                                                     
export PYTHONPATH=/home/nugrid

IPN_URL="https://github.com/swjones/nugridnotebooks.git"
IPN_LOCAL="/home/nugrid/nugridnotebooks"
IPN_DIR="${IPN_LOCAL}/notebooks"

[[ -d ${IPN_DIR} ]] || git clone ${IPN_URL} ${IPN_LOCAL}

ipython notebook \
    --profile=nbserver \
#    --pylab=inline \ # no longer required for ipython 3.1.0
    --no-browser \
    --ip=0.0.0.0 \
    --port=8888 \
    --notebook-dir=${IPN_DIR}

