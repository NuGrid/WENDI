#!/bin/bash

#export PYTHONPATH=/Users/christian/NuGrid/widgets:$PYTHONPATH
#export PYTHONPATH=/Users/christian/NuGrid/widgets/NuGridPy/nugridpy:$PYTHONPATH

PATH_SETUP="/home/nugrid/"
PATH_SETUP="/Users/christian/NuGrid/widgets"

export PYTHONPATH=$PYTHONPATH:$PATH_SETUP

#replacing /home/nugrid to be more general
IP_PROFILE=~/.ipython/profile_nbserver
if ! [ -d "$IP_PROFILE" ]; then ipython profile create nbserver; sleep 5;fi; ##mkdir -v $IP_PROFILE; fi;
ls ~/.ipython/profile_nbserver/startup

IPN_LOCAL=$PATH_SETUP"/WENDI"
NUPYCEE_DIR=$PATH_SETUP"/NuPyCEE"


IPN_URL="https://github.com/NuGrid/WENDI.git"
IPN_DIR="${IPN_LOCAL}/notebooks"
NUPYCEE_URL="https://github.com/NuGrid/NuPyCEE.git"

#get WENDI, for now get my SYGMAwidget branch
[[ -d ${IPN_DIR} ]] || git clone --depth 1 -b  SYGMAwidget ${IPN_URL} ${IPN_LOCAL}

#get NuPyCEE
[[ -d ${NUPYCEE_DIR} ]] || git clone --depth 1 ${NUPYCEE_URL} ${NUPYCEE_DIR}

#get nb_tools.py
wget https://raw.githubusercontent.com/swjones/nugrid-wendocker/master/public-notebook/nb_tools.py

# move startup files from WENDI to IPython profile
echo 'teststest'
ls ${IP_PROFILE}"/startup/"
echo 'ddonee'
cp ${IPN_LOCAL}/startup/* ${IP_PROFILE}/startup/

# add Luke's widget module to python path:
export PYTHONPATH=${IPN_LOCAL}/modules:${NUPYCEE_DIR}:$PYTHONPATH
export SYGMADIR=${NUPYCEE_DIR}

#export JUPYTER_CONFIG_DIR=~/.jupyter/profile_nbserver
#export IPYTHONDIR=$IP_PROFILE

#trus the widget notebooks
jupyter trust \
    ${IPN_DIR}/NuGrid_Set_explorer.ipynb \
    ${IPN_DIR}/SYGMA.ipynb \
    ${IPN_DIR}/OMEGA.ipynb \

jupyter-notebook \
    --no-browser \
    --ip=0.0.0.0 \
    --port=8888 \
    --notebook-dir=${IPN_DIR}
