FROM ubuntu:latest

MAINTAINER Samuel Jones

# scikits.audiolab needs dev stuff
# clean-up unecessary packages once installed.

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get --no-install-recommends install --yes \
    ipython-notebook python-pip \
    python-numpy python-scipy python-matplotlib python-pandas python-sympy \
    python-sklearn hdf5-tools libhdf5-serial-dev python-h5py python-tk \
    build-essential python-dev libsndfile1-dev libsndfile1 git && \
  pip install scikits.audiolab && \
  apt-get remove --yes libsndfile-dev python-dev build-essential && \
  apt-get autoremove --yes && \
  apt-get autoclean --yes && \
  pip install nugridpy vos && \
  pip install https://github.com/jakevdp/JSAnimation/archive/master.zip

# set the lang to avoid issues
RUN apt-get install -y language-pack-en
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure locales

EXPOSE 8080
RUN useradd -d /home/nugrid -m -c "Nugrid Public User" nugrid
ADD ./run-ipython-notebook.bash /home/nugrid/
RUN  chmod +x /home/nugrid/run-ipython-notebook.bash && \ 
     mkdir -p /home/nugrid/CADC/NuGrid && \
     chown -R nugrid:nugrid /home/nugrid 
USER nugrid
ENV HOME /home/nugrid
RUN ipython profile create nbserver
ADD startup.ipy /home/nugrid/.ipython/profile_nbserver/startup/startup.ipy
WORKDIR /home/nugrid
CMD /home/nugrid/run-ipython-notebook.bash
