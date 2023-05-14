FROM python:3.11

WORKDIR /usr/src/

RUN git clone https://github.com/AnnoyingRain5/Relink-LightQuark-Bridge app

WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt
RUN git submodule init; git submodule update --remote

CMD git pull; git submodule update --remote; pip install --no-cache-dir -r requirements.txt; python3 ./lightquark-bridge.py