FROM python:3.7-slim-stretch
RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

WORKDIR /usr/src/app
RUN adduser --disabled-password --gecos "" pyuser
RUN chown -R pyuser:pyuser /usr/src/app

RUN pip3 install face_recognition
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .

USER pyuser:pyuser

EXPOSE 8080
