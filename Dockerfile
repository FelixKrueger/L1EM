FROM mambaorg/micromamba:1.4.1

USER root
WORKDIR /opt/

RUN apt-get update -y && apt-get install -y procps git

RUN \
    micromamba install -y -n base -c bioconda -c conda-forge -c defaults \
    python=2.7.15 bwa=0.7.17 samtools=1.9 numpy=1.14.3 scipy=1.1.0 pysam=0.15.0 bedtools=2.27.1 \
    && micromamba clean -a -y

RUN git clone https://github.com/FelixKrueger/L1EM/ /opt/L1EM
RUN echo 'alias ll="ls -al"' >> ~/.bashrc
RUN cd /opt/L1EM && chmod 755 *.sh && chmod 755 utilities/*.py

ENV L1EM_HOME=/opt/L1EM
ENV PATH="${PATH}:${L1EM_HOME}"
ENV PATH="${PATH}:${L1EM_HOME}/run_L1EM.sh"
