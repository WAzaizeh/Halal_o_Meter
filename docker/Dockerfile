### base image
FROM ubuntu:16.04

### make bash the default shell
SHELL [ "/bin/bash", "--login", "-c" ]

# Create a non-root user
ARG username=aabsi
ARG uid=1000
ARG gid=100
ENV USER $username
ENV UID $uid
ENV GID $gid
ENV HOME /home/$USER
RUN adduser --disabled-password \
    --gecos "Non-root user" \
    --uid $UID \
    --gid $GID \
    --home $HOME \
    $USER

### copy the config files
COPY environment.yml /tmp/
RUN chown $UID:$GID /tmp/environment.yml
COPY docker/entrypoint.sh /usr/local/bin/
RUN chown $UID:$GID /usr/local/bin/entrypoint.sh && \
    chmod u+x /usr/local/bin/entrypoint.sh

### install miniconda as non-root user
# install wget
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
USER $USER
# install miniconda
ENV MINICONDA_VERSION latest
ENV CONDA_DIR $HOME/miniconda3
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-$MINICONDA_VERSION-Linux-x86_64.sh -O ~/miniconda.sh && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh
# make non-activate conda commands available
ENV PATH=$CONDA_DIR/bin:$PATH
# make conda activate command available from /bin/bash --login shells
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile
# make conda activate command available from /bin/bash --interative shells
RUN conda init bash

### create a project directory inside user home
ENV PROJECT_DIR $HOME/app
RUN mkdir $PROJECT_DIR
WORKDIR $PROJECT_DIR

### copy WebApp folder into user's project directory
RUN mkdir web
COPY ./web/ ./web/

### build the conda environment
ENV ENV_PREFIX $PWD/env
RUN conda config --set restore_free_channel true && \
    conda update --name base --channel defaults conda
RUN conda env create --prefix $ENV_PREFIX --file /tmp/environment.yml --force && \
    conda clean --all --yes
RUN conda activate $ENV_PREFIX && \
    cd $CONDA_PREFIX && \
    mkdir -p ./etc/conda/activate.d && \
    mkdir -p ./etc/conda/deactivate.d && \
    touch ./etc/conda/activate.d/env_vars.sh && \
    touch ./etc/conda/deactivate.d/env_vars.sh
# set environment variables necessary for steamlit
COPY ~/miniconda3/envs/sm_project/etc/conda/activate.d/env_vars.sh $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
COPY $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
# deactivate conda env
RUN conda deactivate

### confirm conda environment is activated
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

### default command will launch streamlit app
# exposing default port for streamlit
EXPOSE 8501
# cmd to launch app when container is run
CMD ["streamlit", "run", "./web/st_grid.py"]
